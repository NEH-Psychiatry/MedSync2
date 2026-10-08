"""Pure calculation logic for medication refill-date synchronization.

The module deliberately has no Streamlit dependency. This keeps the calculation
portable, deterministic, and straightforward to test.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

type NumberLike = Decimal | int | float | str

ZERO = Decimal("0")
DEFAULT_MAX_COVERAGE_DAYS = 366
MAX_MEDICATION_LABEL_LENGTH = 100


def _as_decimal(value: NumberLike, *, field_name: str) -> Decimal:
    """Convert a supported numeric value to a finite ``Decimal``."""
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be a number, not a Boolean value.")

    try:
        normalized = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a valid number.") from exc

    if not normalized.is_finite():
        raise ValueError(f"{field_name} must be finite.")

    return normalized.normalize()


def _as_label(value: object, *, field_name: str) -> str:
    """Validate and normalize a human-readable label."""
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be text.")

    cleaned_value = value.strip()
    if not cleaned_value:
        raise ValueError("Each medication needs a non-empty label.")
    if len(cleaned_value) > MAX_MEDICATION_LABEL_LENGTH:
        raise ValueError(
            f"Medication labels must be {MAX_MEDICATION_LABEL_LENGTH} characters or fewer."
        )
    if any(character in cleaned_value for character in "\r\n\t"):
        raise ValueError("Medication labels cannot contain tabs or line breaks.")

    return cleaned_value


def _as_date(value: object, *, field_name: str) -> date:
    """Normalize a date-like input while discarding a datetime's clock value."""
    if isinstance(value, datetime):
        return value.date()
    if not isinstance(value, date):
        raise ValueError(f"{field_name} must be a date.")
    return value


def _as_bool(value: object, *, field_name: str) -> bool:
    """Validate a Boolean input without accepting integer substitutes."""
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be a Boolean value.")
    return value


def _as_nonnegative_int(value: object, *, field_name: str) -> int:
    """Validate a nonnegative integer while rejecting Boolean values."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field_name} must be an integer.")
    if value < 0:
        raise ValueError(f"{field_name} cannot be negative.")
    return value


def _display_number(value: Decimal) -> int | float:
    """Return a dataframe-friendly number without changing calculation precision."""
    if value == value.to_integral_value():
        return int(value)
    return float(value)


@dataclass(frozen=True, slots=True)
class Medication:
    """Medication quantities required by the synchronization calculation."""

    name: str
    daily_dose: Decimal
    units_remaining: Decimal

    def __post_init__(self) -> None:
        cleaned_name = _as_label(self.name, field_name="Medication label")
        daily_dose = _as_decimal(self.daily_dose, field_name="Daily dose")
        units_remaining = _as_decimal(self.units_remaining, field_name="Units remaining")

        if daily_dose <= ZERO:
            raise ValueError("Daily dose must be greater than zero.")
        if units_remaining < ZERO:
            raise ValueError("Units remaining cannot be negative.")

        object.__setattr__(self, "name", cleaned_name)
        object.__setattr__(self, "daily_dose", daily_dose)
        object.__setattr__(self, "units_remaining", units_remaining)

    @classmethod
    def from_values(
        cls,
        *,
        name: str,
        daily_dose: NumberLike,
        units_remaining: NumberLike,
    ) -> Medication:
        """Construct a medication while safely normalizing widget values."""
        return cls(
            name=name,
            daily_dose=_as_decimal(daily_dose, field_name="Daily dose"),
            units_remaining=_as_decimal(units_remaining, field_name="Units remaining"),
        )


def _as_medication(value: object) -> Medication:
    """Validate a medication object supplied by an untyped caller."""
    if not isinstance(value, Medication):
        raise ValueError("Every plan entry must be a Medication instance.")
    return value


@dataclass(frozen=True, slots=True)
class SyncPlanItem:
    """One medication's calculated synchronization quantities."""

    name: str
    daily_dose: Decimal
    units_remaining: Decimal
    coverage_days: int
    target_units: Decimal
    approximate_days_on_hand: Decimal
    additional_units_needed: Decimal

    def as_row(self) -> dict[str, object]:
        """Return a presentation-friendly row for Streamlit."""
        return {
            "Medication": self.name,
            "Daily dose (units/day)": _display_number(self.daily_dose),
            "Units remaining": _display_number(self.units_remaining),
            "Coverage days": self.coverage_days,
            "Target units": _display_number(self.target_units),
            "Approx. days on hand": round(float(self.approximate_days_on_hand), 2),
            "Additional units needed": _display_number(self.additional_units_needed),
        }


def calculate_coverage_days(
    *,
    start_date: date,
    aligned_refill_date: date,
    include_start_date: bool = False,
    include_aligned_refill_date: bool = False,
    max_coverage_days: int = DEFAULT_MAX_COVERAGE_DAYS,
) -> int:
    """Count calendar dates requiring coverage between two endpoints.

    ``include_start_date`` indicates whether the dose on the calculation date is
    still outstanding. ``include_aligned_refill_date`` indicates whether the dose
    on the aligned refill date must be supplied by the current or bridge quantity.
    By default both endpoint doses are excluded. If both endpoints are the same
    calendar date, that date is counted once when either endpoint is included.
    """
    normalized_start = _as_date(start_date, field_name="Calculation date")
    normalized_refill = _as_date(
        aligned_refill_date,
        field_name="Aligned refill date",
    )
    normalized_include_start = _as_bool(
        include_start_date,
        field_name="include_start_date",
    )
    normalized_include_refill = _as_bool(
        include_aligned_refill_date,
        field_name="include_aligned_refill_date",
    )
    normalized_max_days = _as_nonnegative_int(
        max_coverage_days,
        field_name="max_coverage_days",
    )

    if normalized_refill < normalized_start:
        raise ValueError("Aligned refill date must be on or after the calculation date.")

    date_delta = (normalized_refill - normalized_start).days
    if date_delta == 0:
        coverage_days = int(normalized_include_start or normalized_include_refill)
    else:
        coverage_days = (
            date_delta - 1 + int(normalized_include_start) + int(normalized_include_refill)
        )

    if coverage_days > normalized_max_days:
        raise ValueError(
            f"Coverage period cannot exceed {normalized_max_days} days in this calculator."
        )

    return coverage_days


def compute_units_needed(
    *,
    units_remaining: NumberLike,
    daily_dose: NumberLike,
    coverage_days: int,
) -> Decimal:
    """Compute additional units directly, without lossy day-floor conversion."""
    normalized_remaining = _as_decimal(units_remaining, field_name="Units remaining")
    normalized_dose = _as_decimal(daily_dose, field_name="Daily dose")

    if normalized_remaining < ZERO:
        raise ValueError("Units remaining cannot be negative.")
    if normalized_dose <= ZERO:
        raise ValueError("Daily dose must be greater than zero.")

    normalized_coverage_days = _as_nonnegative_int(
        coverage_days,
        field_name="Coverage days",
    )
    target_units = Decimal(normalized_coverage_days) * normalized_dose
    return max(target_units - normalized_remaining, ZERO)


def build_sync_plan(
    medications: Iterable[Medication],
    *,
    start_date: date,
    aligned_refill_date: date,
    include_start_date: bool = False,
    include_aligned_refill_date: bool = False,
    max_coverage_days: int = DEFAULT_MAX_COVERAGE_DAYS,
) -> tuple[SyncPlanItem, ...]:
    """Build a deterministic synchronization plan for one or more medications."""
    medication_list = tuple(_as_medication(item) for item in medications)
    if not medication_list:
        raise ValueError("Add at least one medication before calculating.")

    normalized_labels = [medication.name.casefold() for medication in medication_list]
    if len(normalized_labels) != len(set(normalized_labels)):
        raise ValueError("Medication labels must be unique within a sync plan.")

    coverage_days = calculate_coverage_days(
        start_date=start_date,
        aligned_refill_date=aligned_refill_date,
        include_start_date=include_start_date,
        include_aligned_refill_date=include_aligned_refill_date,
        max_coverage_days=max_coverage_days,
    )

    plan: list[SyncPlanItem] = []
    for medication in medication_list:
        target_units = Decimal(coverage_days) * medication.daily_dose
        additional_units = compute_units_needed(
            units_remaining=medication.units_remaining,
            daily_dose=medication.daily_dose,
            coverage_days=coverage_days,
        )
        approximate_days_on_hand = medication.units_remaining / medication.daily_dose

        plan.append(
            SyncPlanItem(
                name=medication.name,
                daily_dose=medication.daily_dose,
                units_remaining=medication.units_remaining,
                coverage_days=coverage_days,
                target_units=target_units,
                approximate_days_on_hand=approximate_days_on_hand,
                additional_units_needed=additional_units,
            )
        )

    return tuple(plan)
