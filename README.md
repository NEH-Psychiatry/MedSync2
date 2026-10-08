# MedSync2

MedSync2 is a Streamlit-based planning calculator that estimates additional medication units needed between a calculation date and an aligned refill date.

> **Important:** This is a mathematical planning aid, not medical advice or a prescribing/dispensing system. Independently verify every result. Do not enter patient identifiers unless a deployment has been specifically approved for that data.

## Repository guidance

- [`AGENTS.md`](AGENTS.md): coding-agent and contributor guidance, including NEH Texas PMP policy guardrails.
- [`.github/copilot-instructions.md`](.github/copilot-instructions.md): Copilot and Codex compliance instructions.
- [`docs/azure-essentials-operationalization.md`](docs/azure-essentials-operationalization.md): source boundary, operating model, official-resource index, and implementation gates.
- [`docs/cloud-adoption-backlog.md`](docs/cloud-adoption-backlog.md): P0/P1/P2 backlog for issues and pull requests.
- [`docs/architecture/azure-landing-zone-decision-record.md`](docs/architecture/azure-landing-zone-decision-record.md): starter decision record for Azure landing-zone planning.
- [`docs/architecture/identity-and-access-decision-record.md`](docs/architecture/identity-and-access-decision-record.md): starter decision record for the Microsoft Entra ID identity and access model.
- [`.github/ISSUE_TEMPLATE/azure-essentials-task.md`](.github/ISSUE_TEMPLATE/azure-essentials-task.md): issue template for Azure Essentials-aligned work.
- [`.github/ISSUE_TEMPLATE/data-model-task.md`](.github/ISSUE_TEMPLATE/data-model-task.md): issue template for data model and schema changes.
- [`.github/ISSUE_TEMPLATE/vendor-mapping-task.md`](.github/ISSUE_TEMPLATE/vendor-mapping-task.md): issue template for vendor field mapping and integration work.
- [`.github/ISSUE_TEMPLATE/dashboard-metric-task.md`](.github/ISSUE_TEMPLATE/dashboard-metric-task.md): issue template for dashboard metrics and KPI work.
- [`.github/ISSUE_TEMPLATE/compliance-review-task.md`](.github/ISSUE_TEMPLATE/compliance-review-task.md): issue template for compliance review requests.
- [`.github/pull_request_template.md`](.github/pull_request_template.md): pull request checklist including compliance-sensitive items.

## Approved operating posture

The owner-approved target posture is:

- internal/intranet use only;
- private GitHub repository;
- approved internal users only;
- synthetic or non-identifiable entries only;
- no prescribing, dispensing, medication-ordering, or clinical-decision use;
- automatic pull-request merge only after required checks pass.

Repository visibility and platform protection settings must be confirmed in GitHub administration. See [`docs/owner-decisions-2026-07-24.md`](docs/owner-decisions-2026-07-24.md).

## Hardened baseline

- Date-only calculations eliminate clock-time off-by-one behavior.
- Direct unit arithmetic eliminates floor-division overestimation.
- Fractional doses and remaining quantities use `Decimal` precision.
- Calculation logic is separated from the Streamlit presentation layer.
- Endpoint inclusion is explicit for both the calculation date and aligned refill date.
- Validation, regression tests, app tests, linting, typing, security scanning, dependency auditing, CodeQL, dependency review, Dependabot, and container hardening are included.
- Privacy, clinical, deployment, and compliance limitations are explicit.
- Runtime and development dependency locks are generated with hashes and verified by an isolated GitHub Actions workflow.

## Calculation model

Coverage days are the calendar dates whose doses must be supplied by the entered on-hand or bridge quantity.

- The calculation-date dose is excluded by default and included only when it remains outstanding.
- The aligned-refill-date dose is excluded by default and included only when the bridge quantity must cover it.
- When the dates differ, dates strictly between them are always counted.
- When both dates are the same, that calendar date is counted once when either endpoint option is selected.

For each medication:

```text
target units = coverage days * daily dose
additional units = max(target units - units remaining, 0)
```

## Run locally

Requires Python 3.12 or 3.13.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --requirement requirements.txt
streamlit run med_sync_app.py
```

When a reviewed `requirements.lock` is present, prefer the hash-locked installation:

```bash
python -m pip install --require-hashes --requirement requirements.lock
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

## Development checks

```bash
python -m pip install --requirement requirements-dev.txt
python -m ruff check .
python -m ruff format --check .
python -m mypy medsync
python -m bandit -q -r medsync med_sync_app.py
python -m pytest
python -m compileall -q medsync med_sync_app.py tests
python -m pip_audit --requirement requirements.txt
```

When a reviewed `requirements-dev.lock` is present, install it with:

```bash
python -m pip install --require-hashes --requirement requirements-dev.lock
```

## Container

```bash
docker build -t medsync2 .
docker run --rm -p 8501:8501 medsync2
```

Then open `http://localhost:8501` from an approved internal network path only. This is a development and controlled internal-evaluation artifact, not an approved production deployment. See [`docs/architecture/container-deployment-baseline.md`](docs/architecture/container-deployment-baseline.md) for its security, cost, reliability, data, and compliance assumptions and cloud-backlog gates.

## Repository layout

- `med_sync_app.py`: Streamlit presentation layer.
- `medsync/calculator.py`: pure validation and calculation logic.
- `tests/`: regression and Streamlit application tests.
- `docs/architecture/application-design.md`: application contract, boundaries, and exclusions.\n- `docs/architecture/container-deployment-baseline.md`: container security, cost, reliability, data, compliance, and production-blocking assumptions.
- `docs/code-review-and-hardening-report-2026-07-21.md`: review findings, remediation, and residual risks.
- `docs/release-readiness-checklist.md`: pre-merge and pre-deployment gate.
- `docs/owner-decisions-2026-07-24.md`: owner-approved license, use, review, merge, and visibility decisions.
- `SECURITY.md`: security reporting and production-control requirements.
- `LICENSE`: MIT license.
- `docs/azure-essentials-operationalization.md`: existing cloud-adoption governance and source boundary.
- `docs/cloud-adoption-backlog.md`: existing cloud implementation backlog.
- `docs/architecture/azure-landing-zone-decision-record.md`: existing pre-production Azure decision scaffold.

## Privacy and compliance boundary

The repository does not currently implement authentication, authorization, persistent storage, audit logging, or a regulated production environment. The application code does not intentionally persist entries, but hosted use transmits values between browser and server.

The approved current use is internal/intranet with synthetic or non-identifiable data. Private repository visibility does not replace application-level access control, TLS, data governance, or deployment hardening. See `SECURITY.md` before deployment.

No claim of HIPAA, HITRUST, SOC 2, FedRAMP, medical-device, clinical-validation, or other compliance status is made.

## Known limitations

This calculator does not account for variable dosing, PRN use, tapers, adherence, package sizes, insurance restrictions, controlled-substance rules, pharmacy policies, or clinical appropriateness. It does not choose dispensing increments or round quantities for a pharmacy.

The owner has not required a separate external clinical/pharmacy review for the current internal, calculation-only use case. Expansion into patient-specific, prescribing, dispensing, pharmacy-workflow, payer, or clinical-decision use reopens that review requirement.

## Azure Essentials operating model

The repository's existing cloud-adoption package organizes future cloud work into three stages:

1. **Readiness and foundation:** identity, environments, landing zone, cost baseline, repository controls, and data assumptions.
2. **Design and govern:** architecture, policy, review gates, AI guardrails, and deployment decisions.
3. **Manage and optimize:** observability, reliability, backup and restore, cost review, and ongoing remediation.

Azure guidance informs planning; final implementation decisions still require current Microsoft documentation, actual product requirements, and approved data/compliance assumptions.

## License

MedSync2 is licensed under the [MIT License](LICENSE).
