## Summary

Describe what changed and why it matters for MedSync2.

## Change type

- [ ] Calculation or validation logic
- [ ] Streamlit user interface
- [ ] Tests or engineering tooling
- [ ] Security, privacy, or compliance documentation
- [ ] Cloud or deployment architecture
- [ ] Documentation only

## Calculation and safety review

- [ ] Date inclusion/exclusion semantics are explicit
- [ ] Direct unit arithmetic is preserved
- [ ] Fractional quantities are handled with `Decimal` in core logic
- [ ] New or changed behavior has regression tests
- [ ] No patient data, secrets, or medication-entry logging was added
- [ ] User-facing text is not medical advice or a dispensing directive
- [ ] Not applicable

## Azure Essentials lifecycle stage

- [ ] Readiness and foundation
- [ ] Design and govern
- [ ] Manage and optimize
- [ ] Not applicable

## Source boundary

- [ ] Source-derived Azure point
- [ ] Current Microsoft documentation
- [ ] MedSync2-specific implementation decision
- [ ] General cloud-market analysis
- [ ] Not applicable

## Compliance sensitivity

Check every box that applies from the first six options. If one or more of the first six options is checked, add the `compliance-review-required` label and a compliance reviewer; compliance approval is required before merge.

- [ ] Touches PMP workflow logic or PDMP integration
- [ ] Encodes or modifies prescribing authority rules (PMHNP, MD, DO, PA, NP)
- [ ] References controlled-substance scheduling (Schedule II–V)
- [ ] Adds or changes patient-identifier handling, tokenization, or de-identification
- [ ] Modifies dashboard mart queries or reporting exports that could surface PHI
- [ ] Adds or changes a compliance flag, audit log field, or attestation record
- [ ] None of the above — valid only when none of the first six options apply

## PHI and data safety

- [ ] No real patient data (names, MRNs, DOBs, SSNs, diagnoses) is present
- [ ] All test fixtures use synthetic or clearly fake data
- [ ] Any new PHI-bearing field is annotated with `# PHI: <description>`
- [ ] Raw patient identifiers are not passed through marts, dashboards, or reports

## Policy logic

- [ ] No policy rules are invented or extrapolated without a verified citation
- [ ] Unverified policy assumptions are marked `TODO(compliance): <description>`
- [ ] Unknown vendor/source fields are marked `TODO(vendor):` or `TODO(source):`

## Compliance checklist

_Complete every item that applies. PRs touching clinical rules, PDMP logic, prescribing authority, or de-identification cannot merge without these._

- [ ] No PHI or real patient identifiers committed (source code, tests, fixtures, docs, comments)
- [ ] No regulatory or clinical rules encoded without an explicit source citation or `TODO(compliance):` marker
- [ ] All unknown vendor fields or PDMP data elements marked with `TODO(vendor-mapping):` or `TODO(source-unknown):`
- [ ] Dashboard mart queries and analytics views use de-identified or tokenized references only
- [ ] Prescribing authority logic does not grant standalone Schedule II authority to outpatient PMHNPs
- [ ] PDMP workflow correctly distinguishes score-only retrieval from full report review
- [ ] `compliance-review-required` label added and designated reviewer tagged if this PR modifies clinical decision rules, PDMP queries, prescribing authority checks, or de-identification logic

## Risk review

- [ ] Security assumptions documented
- [ ] Cost assumptions documented
- [ ] Reliability assumptions documented
- [ ] Compliance assumptions documented
- [ ] Architecture decision record updated if needed (`docs/architecture/`)

## Testing or validation

Describe the checks performed.

## Open follow-ups

List any remaining work, known limitations, or unresolved `TODO(compliance):` items.
