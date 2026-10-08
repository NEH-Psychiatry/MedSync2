"""MedSync2 calculation package."""

from medsync.calculator import (
    DEFAULT_MAX_COVERAGE_DAYS,
    Medication,
    SyncPlanItem,
    build_sync_plan,
    calculate_coverage_days,
    compute_units_needed,
)

__all__ = [
    "DEFAULT_MAX_COVERAGE_DAYS",
    "Medication",
    "SyncPlanItem",
    "build_sync_plan",
    "calculate_coverage_days",
    "compute_units_needed",
]

__version__ = "0.2.0"
