# MedSync2 Coding-Agent Guidance

## Repository mission

MedSync2 is a calculation-only Streamlit application for estimating medication units required until a refill synchronization date. Preserve the distinction between mathematical planning and clinical, prescribing, dispensing, legal, or compliance decisions.

## NEH Texas PMP policy guardrails

The following rules are **hard constraints** that apply to every agent, Codex task, Copilot suggestion, and human contribution. Violations require a mandatory compliance reviewer signoff before merge.

### Absolute prohibitions

1. **Never encode independent outpatient PMHNP Schedule II signing authority.** Do not write code, configuration, logic, or documentation that grants a psychiatric-mental-health nurse practitioner independent authority to prescribe or sign Schedule II controlled substances in an outpatient setting under Texas law unless a verified, current Texas statutory or regulatory citation is supplied and reviewed by a compliance owner.
2. **Never count a score-only PDMP workflow as a full report review by default.** Accessing a risk score or summary does not satisfy the Texas PDMP full-report review requirement. Any workflow that records PDMP compliance must distinguish between score-only access and full-report review. Do not conflate the two without an explicit, reviewed policy decision.
3. **Never expose raw patient identifiers in dashboard marts or reporting layers.** Patient names, MRNs, dates of birth, SSNs, and other direct identifiers must be removed or tokenized before data reaches any analytics mart, dashboard query, or reporting export. Use surrogate keys or de-identification functions; never pass raw PHI through mart or dashboard layers.

### PHI and sensitive data rules

- **No PHI in the repository.** Do not commit real patient names, MRNs, dates of birth, addresses, diagnoses, medication records, insurance identifiers, or any other Protected Health Information to source code, configuration files, tests, fixtures, or documentation.
- Use synthetic or clearly labeled fake data for all examples, tests, and fixtures.
- If a field name or schema column could hold PHI, annotate it with a `# PHI: <description>` comment and document the de-identification or access-control mechanism in the relevant architecture decision record.

### No invented policy rules

- Do not invent, assume, or extrapolate Texas PMP, DEA, or HIPAA policy rules from general knowledge. If the exact policy text is not available in the repository or linked reference, add a `TODO(compliance): verify <rule description>` comment and open a compliance review issue before implementing the logic.
- Do not add compliance claims (HIPAA, HITRUST, SOC 2, FedRAMP, PDMP) without verified scope, evidence, and owner approval.

### TODOs over assumptions

- When a source field, vendor field, policy rule, or data mapping is unknown or unverified, add a `TODO(source): <description of what needs verification>` comment rather than making an assumption.
- Mark every unverified vendor-specific field with `TODO(vendor): confirm field name and semantics with <vendor name>`.
- Do not silently default to a value that may carry clinical or legal significance. Make the assumption visible.

### Small PRs and compliance reviewer signoff

- Keep pull requests small and focused on a single concern. Avoid mixing policy logic, data model changes, and infrastructure changes in one PR.
- Any PR that touches PMP workflow logic, PDMP integration, prescribing authority rules, controlled-substance scheduling, or patient-identifier handling **must** include a compliance reviewer in the reviewers list and must not be merged without their approval.
- Add `compliance-review-required` as a label on any such PR.

## Application invariants

1. Keep calculation logic in `medsync/calculator.py`; do not call Streamlit from the core module.
2. Use date-only semantics. Never calculate coverage from `datetime.now()` or a clock-dependent timedelta.
3. Compute unit shortfall directly:
   `max(coverage_days * daily_dose - units_remaining, 0)`.
4. Use `Decimal` for medication quantities and doses.
5. Treat both endpoint doses as explicit inputs. By default, cover only dates strictly between the calculation date and aligned refill date.
6. Do not log form entries, medication labels, or results.
7. Do not add autonomous clinical recommendations or represent output as medical advice.
8. Add regression tests for every calculation change.

## Required validation

Before completing a code change, run:

```bash
python -m ruff check .
python -m ruff format --check .
python -m mypy medsync
python -m bandit -q -r medsync med_sync_app.py
python -m pytest
python -m compileall -q medsync med_sync_app.py tests
python -m pip_audit --requirement requirements.txt
```

## Sensitive-data guardrails

- Never place real patient data in code, tests, examples, screenshots, issues, or pull requests.
- Do not hard-code secrets, tenant IDs, subscription IDs, credentials, or environment-specific identifiers.
- Do not claim a deployment is HIPAA, HITRUST, SOC 2, FedRAMP, or otherwise compliant without verified scope, evidence, and approval.
- Any persistence, authentication, audit logging, external integration, or PHI handling requires an architecture/security review.

## Azure Essentials source boundary

When working from Azure Essentials material, keep these categories separate:

1. **Source-derived Azure points**: concepts traceable to the Azure Essentials resource kit or supplied update research.
2. **Current Microsoft documentation**: product names, navigation, pricing, compliance references, and implementation details that must be rechecked at time of use.
3. **MedSync2-specific decisions**: choices made after reviewing the actual code, product requirements, data flows, regulated-data posture, and deployment target.
4. **General cloud-market analysis**: neutral context that must not be represented as a Microsoft source claim.

Before adding cloud infrastructure, AI, compliance, or deployment code:

- update the applicable decision record in `docs/architecture/`;
- link work to `docs/cloud-adoption-backlog.md` or an issue;
- validate it against `docs/azure-essentials-operationalization.md`;
- document security, cost, reliability, data, and compliance assumptions;
- use hyphenated filenames for new user-facing documents, except required platform paths.

## Current Azure terminology baseline

Use current Microsoft terminology unless a legacy name is needed for searchability:

- Microsoft Foundry, formerly Azure AI Foundry.
- Microsoft Entra ID, formerly Azure Active Directory or Azure AD.
- Azure Proactive Resiliency Library v2 when referencing APRL guidance.
- Azure Well-Architected Framework when evaluating workload readiness.
- Azure Monitor Baseline Alerts when standardizing alerting baselines.
- Azure Verified Modules when evaluating reusable Bicep or Terraform modules.

Do not imply that the Azure Essentials source deck directly compares Azure and AWS.

## Pull request checklist

- What MedSync2 capability does this enable?
- Is the change source-derived, current-doc verified, or MedSync2-specific?
- Which Azure Essentials lifecycle stage does it support: readiness and foundation, design and govern, or manage and optimize?
- What security, cost, reliability, and compliance assumptions are introduced?
- What remains unverified or environment-specific?
- Does this PR touch PMP workflow, PDMP integration, prescribing authority, or patient identifiers? If yes, is a compliance reviewer assigned?

## Recommended documents to keep current

- `README.md`: application orientation, calculation contract, and repository links.
- `docs/architecture/application-design.md`: application boundary and deterministic contract.
- `docs/azure-essentials-operationalization.md`: operating model and source boundary.
- `docs/cloud-adoption-backlog.md`: prioritized cloud execution queue.
- `docs/architecture/`: durable application and cloud architecture decisions.
- `docs/release-readiness-checklist.md`: release and deployment gate.
