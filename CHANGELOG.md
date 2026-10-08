# Changelog

All notable changes to MedSync2 should be recorded here.

## Unreleased

### Changed

- Replaced clock-dependent date arithmetic with explicit date-only calculations.
- Replaced floor-division day estimates with direct unit-shortfall arithmetic.
- Separated Streamlit presentation from pure calculation logic.
- Added exact decimal handling for fractional doses and quantities.
- Added independent inclusion controls for calculation-date and aligned-refill-date doses.
- Added explicit validation for labels, dates, quantities, duplicate entries, types, and coverage horizon.

### Added

- Core regression tests and Streamlit AppTest coverage.
- CI, CodeQL, dependency review, Dependabot, security policy, contribution guidance, and issue templates.
- Non-root container build with a health check.
- Hardened Streamlit error-display, telemetry, CORS, and XSRF defaults.
- Architecture, release-readiness, and comprehensive review documentation.
