# Contributing

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --requirement requirements-dev.txt
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

## Required checks

Run these before opening a pull request:

```bash
python -m ruff check .
python -m ruff format --check .
python -m mypy medsync
python -m bandit -q -r medsync med_sync_app.py
python -m pytest
python -m compileall -q medsync med_sync_app.py tests
python -m pip_audit --requirement requirements.txt
```

## Calculation changes

Any change to date or quantity semantics must:

1. document whether the calculation and aligned-refill dates are inclusive or exclusive;
2. add regression tests for same-day, past-date, fractional-dose, and excess-on-hand cases as applicable;
3. preserve direct unit arithmetic rather than converting remaining units to floored whole days;
4. avoid introducing clinical recommendations into the calculation layer.

## Privacy and security

Never use real patient data in examples, tests, screenshots, issues, or pull requests. Do not add logging of form entries or results.

## Pull requests

Keep changes focused, explain assumptions, list validation performed, and identify any remaining deployment or compliance limitations.
