---
name: Compliance review task
description: Request a formal compliance review of policy logic, PHI handling, PDMP workflow, or prescribing authority rules.
title: "[Compliance review]: "
labels: ["compliance-review-required"]
assignees: []
---

## Review request summary

Describe the change, feature, or design decision that requires compliance review and why.

## Trigger

Check the reason this review was requested:

- [ ] PR touches PMP workflow logic or PDMP integration
- [ ] PR encodes or modifies prescribing authority rules (PMHNP, MD, DO, PA, NP)
- [ ] PR references controlled-substance scheduling (Schedule II–V)
- [ ] PR adds or changes patient-identifier handling, tokenization, or de-identification
- [ ] PR modifies dashboard mart queries or reporting exports that could surface PHI
- [ ] PR adds or changes a compliance flag, audit log field, or attestation record
- [ ] Proactive review requested before implementation begins

## Policy areas in scope

Check all that apply:

- [ ] Texas PMP prescriber requirements
- [ ] Texas PDMP (PMP InterConnect / AWARxE) full-report review requirement
- [ ] PMHNP prescribing authority under Texas Occupations Code
- [ ] DEA Schedule II–V rules
- [ ] HIPAA minimum necessary and PHI de-identification
- [ ] Other (describe below)

## Specific questions for the compliance reviewer

List each question that requires a verified answer before or during implementation. If you do not have the answer, write `TODO(compliance): <question>`.

1.
2.
3.

## Known guardrail risks

- [ ] Risk of encoding PMHNP independent Schedule II authority — reviewed and mitigated
- [ ] Risk of conflating score-only PDMP access with full-report review — reviewed and mitigated
- [ ] Risk of exposing raw patient identifiers in mart or reporting layer — reviewed and mitigated

## Evidence and references

Add links to relevant Texas statutes, DEA regulations, HIPAA guidance, internal policy documents, vendor specs, or related issues.

## Reviewer

Assign a compliance owner with authority to approve or reject the policy logic. Do not merge the related PR without this reviewer's explicit approval.

## Acceptance criteria

- [ ] All specific compliance questions answered with verified citations
- [ ] Guardrail risks assessed and disposition documented
- [ ] `TODO(compliance):` items in related PR resolved or deferred with justification
- [ ] Related PR labeled `compliance-review-required` and this reviewer added
- [ ] Compliance owner has approved the related PR

## Notes
