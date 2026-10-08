"""Headless smoke and interaction tests for the Streamlit interface."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

try:
    from streamlit.testing.v1 import AppTest
except ModuleNotFoundError:
    AppTest = None  # type: ignore[assignment,misc]

APP_PATH = Path(__file__).resolve().parents[1] / "med_sync_app.py"


def _app() -> AppTest:
    assert AppTest is not None
    app = AppTest.from_file(APP_PATH, default_timeout=10).run()
    assert not app.exception
    return app


@pytest.mark.skipif(AppTest is None, reason="Streamlit is not installed")
def test_initial_render_is_safe_and_complete() -> None:
    app = _app()

    assert app.title[0].value == "Medication Sync Calculator"
    assert len(app.warning) == 1
    assert len(app.caption) >= 1
    assert len(app.text_input) == 1
    assert app.button[0].label == "Calculate sync plan"


@pytest.mark.skipif(AppTest is None, reason="Streamlit is not installed")
def test_blank_medication_label_displays_validation_error() -> None:
    app = _app()

    app.button[0].click().run()

    assert not app.exception
    assert len(app.error) == 1
    assert "non-empty label" in app.error[0].value


@pytest.mark.skipif(AppTest is None, reason="Streamlit is not installed")
def test_valid_submission_renders_correct_direct_unit_shortfall() -> None:
    app = _app()
    app.date_input(key="calculation-date").set_value(date(2026, 7, 21))
    app.date_input(key="aligned-refill-date").set_value(date(2026, 7, 24))
    app.text_input(key="medication-name-0").set_value("Example medication")
    app.number_input(key="daily-dose-0").set_value(3.0)
    app.number_input(key="units-remaining-0").set_value(5.0)

    app.button[0].click().run()

    assert not app.exception
    assert not app.error
    assert len(app.dataframe) == 1
    result = app.dataframe[0].value
    assert result.loc[0, "Coverage days"] == 2
    assert result.loc[0, "Target units"] == 6
    assert result.loc[0, "Additional units needed"] == 1


@pytest.mark.skipif(AppTest is None, reason="Streamlit is not installed")
def test_past_aligned_refill_date_displays_validation_error() -> None:
    app = _app()
    app.date_input(key="calculation-date").set_value(date(2026, 7, 22))
    app.date_input(key="aligned-refill-date").set_value(date(2026, 7, 21))
    app.text_input(key="medication-name-0").set_value("Example medication")

    app.button[0].click().run()

    assert not app.exception
    assert len(app.error) == 1
    assert "on or after" in app.error[0].value
