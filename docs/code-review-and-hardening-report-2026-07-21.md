# Comprehensive Code Review and Hardening Report

Review date: 2026-07-21
Repository: `cvassat/MedSync2`
Reviewed branch: `main` at `b5f84c3b28e9337adab3c4f6d5b230e91c7c0872`

## Executive verdict

The original application was a useful prototype but not release-ready. Its primary calculation had two material correctness defects: clock-time truncation in date subtraction and overestimation caused by converting remaining units to floored whole days. The application also coupled Streamlit rendering to business logic and lacked tests, CI, dependency controls, security guidance, and an executable deployment baseline.

The hardened baseline remediates the calculation defects and establishes a testable, bounded calculation contract. It adds engineering and security controls appropriate to a small calculation-only application. It does **not** make the application suitable for protected health information or establish regulatory compliance.

## Findings and disposition

| Area | Original condition | Severity | Disposition |
|---|---|---:|---|
| Date arithmetic | Subtracted `datetime.today()` from a midnight sync datetime and read truncated `.days` | High | Replaced with explicit date-only arithmetic and injectable calculation date |
| Unit arithmetic | Floored `remaining // daily_dose`, then converted back to units | High | Replaced with direct unit-shortfall calculation |
| Endpoint semantics | It was unclear whether calculation-date and target-date doses were included | High | Added independent, explicit endpoint options and tests |
| Error handling | Core function called `st.error()` and returned an empty list | Medium | Core raises validation errors; UI renders them |
| Numeric precision | Integer-only inputs and implicit arithmetic | Medium | Added `Decimal` normalization and fractional quantity support |
| Input validation | Missing label validation and limited boundary checks | Medium | Added label, uniqueness, dose, quantity, date-order, type, and horizon validation |
| Testability | No automated tests | High | Added deterministic unit/regression tests and headless Streamlit AppTest coverage |
| Dependency control | `streamlit>=1.0.0` allowed unbounded upgrades | High | Pinned reviewed direct dependencies; added Dependabot and pip-audit |
| CI/security | No automated quality or security gate | High | Added lint, format, type, security, test, compile, audit, dependency-review, and CodeQL workflows |
| Privacy messaging | No data-classification or identifiable-data warning | High | Added no-identifiers guidance and explicit hosted-transmission boundary |
| Deployment | No repeatable runtime definition | Medium | Added non-root Docker image, health check, and hardened Streamlit defaults |
| Governance | Cloud guidance existed but was disconnected from executable application controls | Medium | Integrated application invariants, release gate, security policy, and architecture contract |

## Implemented calculation contract

Coverage days are the calendar dates whose doses must be supplied by the entered on-hand or bridge quantity.

- Calculation-date dose: excluded by default; explicitly includable.
- Aligned-refill-date dose: excluded by default; explicitly includable.
- Dates strictly between the endpoints: always counted.
- Same-day endpoints: the single calendar date is counted once when either endpoint flag is selected.

For each medication:

```text
target units = coverage days * daily dose
additional units = max(target units - units remaining, 0)
```

## Validation performed in the review environment

- Pytest: **25 core tests passed** and **4 Streamlit interaction tests skipped locally** because Streamlit was not installed.
- Standard-library unittest discovery: **25 passed**.
- Python bytecode compilation: passed.
- Python AST parsing: passed.
- TOML and YAML parsing: passed.
- Static scan for the original defect patterns: passed after remediation.
- Static scan for obvious hard-coded credential assignments: no finding.
- Python line-length check: passed.

The review environment did not have the project development dependencies installed, so Ruff, Mypy, Bandit, pip-audit against the project environment, Streamlit AppTest execution, and Docker build execution are delegated to the included CI workflow. A host-level `pip check` finding involved unrelated preinstalled packages and is not a MedSync2 dependency result.

## Residual risks and required owner decisions

1. **Clinical and dispensing scope:** The formula does not account for variable schedules, tapers, PRN use, adherence, package sizes, refill limits, insurance rules, controlled-substance restrictions, or pharmacy policy.
2. **Regulated data:** There is no approved authentication, authorization, audit, retention, incident-response, or regulated hosting implementation. Do not use identifiable patient data.
3. **Dependency reproducibility:** Direct dependencies are pinned, but a fully hashed transitive lock should be generated and reviewed in the target build environment.
4. **Repository license:** No license selection was evident in the reviewed repository. The owner must choose one before external reuse or distribution.
5. **Repository settings:** Branch protection, required checks, secret scanning, and other GitHub settings cannot be guaranteed by committed files alone.
6. **Cloud architecture:** Existing Azure records remain draft. Production deployment requires completed identity, data-protection, observability, cost, and landing-zone decisions.
7. **Independent domain validation:** Calculation assumptions and examples should be independently reviewed by intended clinical/pharmacy stakeholders before operational use.

## Release recommendation

The hardened baseline is suitable for pull-request review and controlled non-production testing with synthetic data. Production or identifiable-data use remains blocked until the residual risks above have named owners and documented acceptance or remediation.
