# MedSync2 Release Readiness Checklist

Use this gate before merging or deploying a release.

## Owner-approved baseline — 2026-07-24

- License: MIT.
- Intended use: internal/intranet only.
- Repository visibility target: private.
- Data boundary: synthetic or non-identifiable entries only.
- Separate external clinical/pharmacy review: not required for the current calculation-only, non-clinical-decision scope.
- Merge behavior: automatic only after required checks pass.
- Proceed with the hardened baseline: approved.

See `docs/owner-decisions-2026-07-24.md`. These decisions do not authorize identifiable data or establish compliance or clinical-validation status.

## Application behavior

- [ ] Date inclusion/exclusion semantics are unchanged or explicitly reviewed.
- [ ] Direct unit arithmetic remains `max(coverage days × daily dose - units remaining, 0)`.
- [ ] Fractional quantities remain exact in the calculation layer.
- [ ] Same-day, past-date, excess-on-hand, and non-divisible-quantity cases pass.
- [ ] User-facing text does not imply prescribing, dispensing, legal, or clinical advice.

## Automated assurance

- [ ] `python -m ruff check .`
- [ ] `python -m ruff format --check .`
- [ ] `python -m mypy medsync`
- [ ] `python -m bandit -q -r medsync med_sync_app.py`
- [ ] `python -m pytest`
- [ ] `python -m compileall -q medsync med_sync_app.py tests`
- [ ] `python -m pip_audit --requirement requirements.txt`
- [ ] Runtime and development locks are generated on Python 3.12 with hashes.
- [ ] `python -m pip install --require-hashes --requirement requirements-dev.lock` succeeds.
- [ ] CodeQL completes without unresolved high-severity findings.
- [ ] Dependency review passes for introduced or changed dependencies.
- [ ] Dependabot alerts and version-update pull requests are triaged.

## Privacy and security

- [ ] Repository visibility is confirmed private.
- [ ] No patient data, credentials, secrets, or environment identifiers appear in the diff.
- [ ] Form values and results are not logged.
- [ ] Browser error details remain suppressed outside controlled development environments.
- [ ] CORS and XSRF protections remain enabled.
- [ ] TLS is terminated by an approved ingress, proxy, or managed platform.
- [ ] Access is limited to approved internal users and an approved internal network path.
- [ ] Authentication and authorization are approved before any identifiable-data use.
- [ ] Retention, logging, incident-response, and evidence ownership are documented before identifiable-data production use.

## Deployment

- [ ] Public internet exposure is disabled.
- [ ] Container runs as a non-root user.
- [ ] Health check passes.
- [ ] Runtime dependency audit passes against the final image or environment.
- [ ] Environment promotion and rollback are documented.
- [ ] Cookie secret and other deployment secrets are injected through approved secret management.
- [ ] The Azure landing-zone and data-protection decision records are completed or formally deferred before production-like deployment.

## Governance

- [x] Approved MIT license is present.
- [ ] Branch protection and required status checks are enabled for `main`.
- [ ] Repository auto-merge is enabled.
- [ ] CI, CodeQL, dependency-review, and lock-generation checks are required.
- [ ] Secret scanning and dependency graph features are enabled where supported.
- [ ] Generated lock files are reviewed and committed.
- [ ] Residual risks are accepted by an identified owner.
