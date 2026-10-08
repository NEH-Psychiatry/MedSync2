"""Streamlit interface for the MedSync2 calculation engine."""

from __future__ import annotations

from datetime import date, timedelta

import streamlit as st

from medsync import DEFAULT_MAX_COVERAGE_DAYS, Medication, build_sync_plan

MAX_MEDICATIONS = 10
DEFAULT_SYNC_OFFSET_DAYS = 30
QUANTITY_STEP = 0.01


def _build_medications(
    raw_medications: list[tuple[str, float, float]],
) -> tuple[Medication, ...]:
    """Convert Streamlit widget values to validated domain objects."""
    return tuple(
        Medication.from_values(
            name=name,
            daily_dose=daily_dose,
            units_remaining=units_remaining,
        )
        for name, daily_dose, units_remaining in raw_medications
    )


def main() -> None:
    """Render the MedSync2 Streamlit application."""
    st.set_page_config(
        page_title="Medication Sync Calculator",
        page_icon="📅",
        layout="centered",
    )

    st.title("Medication Sync Calculator")
    st.write(
        "Estimate additional medication units needed between a calculation date and an "
        "aligned refill date."
    )
    st.warning(
        "Planning calculator only. It does not evaluate clinical appropriateness, "
        "prescription legality, insurance rules, packaging, or pharmacy dispensing "
        "requirements. Verify all quantities independently."
    )
    st.caption(
        "Avoid patient names, dates of birth, medical-record numbers, or other identifiers. "
        "The application code does not intentionally persist entries, but a hosted "
        "deployment still transmits them between the browser and server."
    )

    with st.form("medication-sync-form"):
        date_columns = st.columns(2)
        calculation_date = date_columns[0].date_input(
            "Calculation date",
            value=date.today(),
            help="The date from which coverage is calculated.",
            format="YYYY-MM-DD",
            key="calculation-date",
        )
        aligned_refill_date = date_columns[1].date_input(
            "Aligned refill date",
            value=date.today() + timedelta(days=DEFAULT_SYNC_OFFSET_DAYS),
            help="The date the synchronized refill is expected to become available.",
            format="YYYY-MM-DD",
            key="aligned-refill-date",
        )

        endpoint_columns = st.columns(2)
        include_calculation_date = endpoint_columns[0].checkbox(
            "Include calculation-date dose",
            value=False,
            help=(
                "Enable this when the dose on the calculation date has not yet been taken. "
                "Leave it off when that day's dose is already accounted for."
            ),
            key="include-calculation-date",
        )
        include_aligned_refill_date = endpoint_columns[1].checkbox(
            "Include aligned-refill-date dose",
            value=False,
            help=(
                "Enable this only when the current or bridge supply must cover the dose on the "
                "aligned refill date. Leave it off when the refill will be available first."
            ),
            key="include-aligned-refill-date",
        )

        medication_count = st.number_input(
            "Number of medications",
            min_value=1,
            max_value=MAX_MEDICATIONS,
            value=1,
            step=1,
            help=f"Enter between 1 and {MAX_MEDICATIONS} medications.",
            key="medication-count",
        )

        raw_medications: list[tuple[str, float, float]] = []
        for index in range(int(medication_count)):
            with st.container(border=True):
                st.subheader(f"Medication {index + 1}")
                medication_name = st.text_input(
                    "Medication label",
                    key=f"medication-name-{index}",
                    help=(
                        "Use a medication/strength label only; do not include patient "
                        "identifiers. Labels must be unique in this plan."
                    ),
                    placeholder="Example: medication 500 mg",
                )
                quantity_columns = st.columns(2)
                daily_dose = quantity_columns[0].number_input(
                    "Daily dose (units/day)",
                    min_value=QUANTITY_STEP,
                    value=1.0,
                    step=QUANTITY_STEP,
                    format="%.4f",
                    key=f"daily-dose-{index}",
                )
                units_remaining = quantity_columns[1].number_input(
                    "Units remaining",
                    min_value=0.0,
                    value=0.0,
                    step=QUANTITY_STEP,
                    format="%.4f",
                    key=f"units-remaining-{index}",
                )
                raw_medications.append((medication_name, daily_dose, units_remaining))

        submitted = st.form_submit_button("Calculate sync plan", type="primary")

    if not submitted:
        return

    try:
        medications = _build_medications(raw_medications)
        plan = build_sync_plan(
            medications,
            start_date=calculation_date,
            aligned_refill_date=aligned_refill_date,
            include_start_date=include_calculation_date,
            include_aligned_refill_date=include_aligned_refill_date,
            max_coverage_days=DEFAULT_MAX_COVERAGE_DAYS,
        )
    except ValueError as exc:
        st.error(str(exc))
        return

    st.subheader("Sync plan")
    st.caption(
        f"Calculation date: {calculation_date.isoformat()} · "
        f"Aligned refill date: {aligned_refill_date.isoformat()}"
    )
    st.dataframe(
        [item.as_row() for item in plan],
        hide_index=True,
        width="stretch",
    )

    coverage_days = plan[0].coverage_days
    if all(item.additional_units_needed == 0 for item in plan):
        st.success("The entered quantities already cover the selected period.")
    else:
        st.info(
            f"The plan covers {coverage_days} calendar day(s). Use the calculated quantity "
            "only as a planning value; prescribing and dispensing increments require "
            "independent verification."
        )

    with st.expander("Calculation method and assumptions"):
        st.markdown(
            """
- Doses strictly between the calculation date and aligned refill date are included.
- Either endpoint dose is included only when its corresponding checkbox is enabled.
- `target units = coverage days * daily dose`.
- `additional units needed = max(target units - units remaining, 0)`.
- Variable schedules, tapers, as-needed dosing, dose changes, package sizes, refill limits,
  insurance rules, and pharmacy-specific requirements are outside this calculator's scope.
            """
        )


if __name__ == "__main__":
    main()
