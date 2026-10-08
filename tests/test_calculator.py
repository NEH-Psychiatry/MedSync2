"""Regression tests for MedSync2 calculation logic."""

from __future__ import annotations

import unittest
from datetime import date, datetime
from decimal import Decimal

from medsync import Medication, build_sync_plan, calculate_coverage_days, compute_units_needed


class MedicationValidationTests(unittest.TestCase):
    def test_trims_and_normalizes_values(self) -> None:
        medication = Medication.from_values(
            name="  Example medication  ",
            daily_dose="1.50",
            units_remaining="3.00",
        )

        self.assertEqual(medication.name, "Example medication")
        self.assertEqual(medication.daily_dose, Decimal("1.5"))
        self.assertEqual(medication.units_remaining, Decimal("3"))

    def test_rejects_empty_label(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-empty label"):
            Medication.from_values(name="   ", daily_dose=1, units_remaining=0)

    def test_rejects_non_text_label(self) -> None:
        with self.assertRaisesRegex(ValueError, "must be text"):
            Medication(name=123, daily_dose=Decimal("1"), units_remaining=Decimal("0"))  # type: ignore[arg-type]

    def test_rejects_multiline_label(self) -> None:
        with self.assertRaisesRegex(ValueError, "line breaks"):
            Medication.from_values(
                name="Medication\nidentifier",
                daily_dose=1,
                units_remaining=0,
            )

    def test_rejects_zero_dose(self) -> None:
        with self.assertRaisesRegex(ValueError, "greater than zero"):
            Medication.from_values(name="Medication", daily_dose=0, units_remaining=0)

    def test_rejects_nonfinite_dose(self) -> None:
        with self.assertRaisesRegex(ValueError, "must be finite"):
            Medication.from_values(name="Medication", daily_dose="NaN", units_remaining=0)

    def test_rejects_boolean_dose(self) -> None:
        with self.assertRaisesRegex(ValueError, "Boolean"):
            Medication.from_values(name="Medication", daily_dose=True, units_remaining=0)

    def test_rejects_negative_remaining(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            Medication.from_values(name="Medication", daily_dose=1, units_remaining=-1)


class CoverageDaysTests(unittest.TestCase):
    def test_excludes_both_endpoint_doses_by_default(self) -> None:
        days = calculate_coverage_days(
            start_date=date(2026, 7, 21),
            aligned_refill_date=date(2026, 7, 24),
        )

        self.assertEqual(days, 2)

    def test_includes_calculation_date_when_requested(self) -> None:
        days = calculate_coverage_days(
            start_date=date(2026, 7, 21),
            aligned_refill_date=date(2026, 7, 24),
            include_start_date=True,
        )

        self.assertEqual(days, 3)

    def test_includes_aligned_refill_date_when_requested(self) -> None:
        days = calculate_coverage_days(
            start_date=date(2026, 7, 21),
            aligned_refill_date=date(2026, 7, 24),
            include_aligned_refill_date=True,
        )

        self.assertEqual(days, 3)

    def test_includes_both_endpoints_when_requested(self) -> None:
        days = calculate_coverage_days(
            start_date=date(2026, 7, 21),
            aligned_refill_date=date(2026, 7, 24),
            include_start_date=True,
            include_aligned_refill_date=True,
        )

        self.assertEqual(days, 4)

    def test_same_day_counts_once_when_either_endpoint_is_included(self) -> None:
        day = date(2026, 7, 21)
        self.assertEqual(
            calculate_coverage_days(start_date=day, aligned_refill_date=day),
            0,
        )
        self.assertEqual(
            calculate_coverage_days(
                start_date=day,
                aligned_refill_date=day,
                include_start_date=True,
            ),
            1,
        )
        self.assertEqual(
            calculate_coverage_days(
                start_date=day,
                aligned_refill_date=day,
                include_aligned_refill_date=True,
            ),
            1,
        )
        self.assertEqual(
            calculate_coverage_days(
                start_date=day,
                aligned_refill_date=day,
                include_start_date=True,
                include_aligned_refill_date=True,
            ),
            1,
        )

    def test_normalizes_datetime_to_date(self) -> None:
        self.assertEqual(
            calculate_coverage_days(
                start_date=datetime(2026, 7, 21, 23, 59),
                aligned_refill_date=datetime(2026, 7, 23, 0, 1),
                include_start_date=True,
            ),
            2,
        )

    def test_rejects_past_aligned_refill_date(self) -> None:
        with self.assertRaisesRegex(ValueError, "on or after"):
            calculate_coverage_days(
                start_date=date(2026, 7, 22),
                aligned_refill_date=date(2026, 7, 21),
            )

    def test_rejects_excessive_horizon(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot exceed 30 days"):
            calculate_coverage_days(
                start_date=date(2026, 7, 1),
                aligned_refill_date=date(2026, 8, 2),
                include_start_date=True,
                include_aligned_refill_date=True,
                max_coverage_days=30,
            )

    def test_rejects_non_boolean_inclusion_flags(self) -> None:
        with self.assertRaisesRegex(ValueError, "Boolean"):
            calculate_coverage_days(
                start_date=date(2026, 7, 21),
                aligned_refill_date=date(2026, 7, 22),
                include_start_date=1,  # type: ignore[arg-type]
            )
        with self.assertRaisesRegex(ValueError, "Boolean"):
            calculate_coverage_days(
                start_date=date(2026, 7, 21),
                aligned_refill_date=date(2026, 7, 22),
                include_aligned_refill_date=1,  # type: ignore[arg-type]
            )

    def test_rejects_boolean_maximum_horizon(self) -> None:
        with self.assertRaisesRegex(ValueError, "integer"):
            calculate_coverage_days(
                start_date=date(2026, 7, 21),
                aligned_refill_date=date(2026, 7, 22),
                max_coverage_days=True,  # type: ignore[arg-type]
            )


class UnitCalculationTests(unittest.TestCase):
    def test_direct_formula_avoids_floor_division_overestimate(self) -> None:
        result = compute_units_needed(
            units_remaining=5,
            daily_dose=3,
            coverage_days=2,
        )

        self.assertEqual(result, Decimal("1"))

    def test_supports_fractional_doses_exactly(self) -> None:
        result = compute_units_needed(
            units_remaining="0.5",
            daily_dose="0.75",
            coverage_days=3,
        )

        self.assertEqual(result, Decimal("1.75"))

    def test_never_returns_negative_quantity(self) -> None:
        result = compute_units_needed(
            units_remaining=20,
            daily_dose=2,
            coverage_days=5,
        )

        self.assertEqual(result, Decimal("0"))

    def test_rejects_boolean_coverage_days(self) -> None:
        with self.assertRaisesRegex(ValueError, "integer"):
            compute_units_needed(
                units_remaining=0,
                daily_dose=1,
                coverage_days=True,
            )


class BuildPlanTests(unittest.TestCase):
    def test_builds_plan_and_preserves_order(self) -> None:
        medications = (
            Medication.from_values(name="First", daily_dose=2, units_remaining=1),
            Medication.from_values(name="Second", daily_dose="0.5", units_remaining=0),
        )

        plan = build_sync_plan(
            medications,
            start_date=date(2026, 7, 21),
            aligned_refill_date=date(2026, 7, 24),
            include_start_date=True,
        )

        self.assertEqual([item.name for item in plan], ["First", "Second"])
        self.assertEqual(plan[0].coverage_days, 3)
        self.assertEqual(plan[0].target_units, Decimal("6"))
        self.assertEqual(plan[0].additional_units_needed, Decimal("5"))
        self.assertEqual(plan[1].additional_units_needed, Decimal("1.5"))

    def test_rejects_duplicate_labels_case_insensitively(self) -> None:
        medications = (
            Medication.from_values(name="Medication A", daily_dose=1, units_remaining=0),
            Medication.from_values(name="medication a", daily_dose=1, units_remaining=0),
        )

        with self.assertRaisesRegex(ValueError, "must be unique"):
            build_sync_plan(
                medications,
                start_date=date(2026, 7, 21),
                aligned_refill_date=date(2026, 7, 22),
            )

    def test_rejects_empty_medication_collection(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least one"):
            build_sync_plan(
                (),
                start_date=date(2026, 7, 21),
                aligned_refill_date=date(2026, 7, 22),
            )

    def test_rejects_non_medication_entries(self) -> None:
        with self.assertRaisesRegex(ValueError, "Medication instance"):
            build_sync_plan(
                (object(),),  # type: ignore[arg-type]
                start_date=date(2026, 7, 21),
                aligned_refill_date=date(2026, 7, 22),
            )


if __name__ == "__main__":
    unittest.main()
