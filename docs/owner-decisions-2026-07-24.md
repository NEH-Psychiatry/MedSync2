# MedSync2 Owner Decision Record

Date: 2026-07-24

Applies to: pull request #13 and the hardened MedSync2 baseline

## Approved decisions

| Decision area | Owner decision | Implementation consequence |
|---|---|---|
| Repository license | MIT | Add the standard MIT license with 2026 copyright attribution to Codie Vassar. |
| Hashed dependency locks | Yes | Generate fully resolved, hash-locked runtime and development dependency files on Python 3.12 and verify installation with `--require-hashes`. |
| Separate external clinical/pharmacy review | None required for the current intended use | Record this as an owner risk decision for an internal, calculation-only planning tool. It is not evidence of clinical validation and does not authorize prescribing, dispensing, or clinical-decision use. |
| Intended use | Internal/intranet | Do not expose the application to the public internet. Limit access to approved internal users and synthetic or non-identifiable entries. |
| Merge behavior | Automatic after required checks pass | Enable pull-request auto-merge when repository settings permit it. Required checks remain a merge gate. |
| Repository visibility | Private | Convert or maintain the GitHub repository as private through repository administration settings. |
| Proceed with the hardened baseline | Yes | Complete the documented changes, verify checks, and merge only after the private/internal boundary and required controls are confirmed. |

## Data and use boundary

The approved internal/intranet posture does not authorize protected or identifiable patient data. Until authentication, authorization, logging/retention, incident-response, and approved hosting controls are implemented:

- do not enter patient names, dates of birth, medical-record numbers, addresses, or other identifiers;
- do not use the calculator as a prescribing, dispensing, medication-ordering, or clinical-decision system;
- do not persist or log entered medication data or calculation results;
- use synthetic or non-identifiable examples only;
- keep the service behind approved private access controls and TLS.

## Clinical-review disposition

The owner has determined that no separate external clinical/pharmacy review is required for the current internal, non-clinical-decision use case. The calculation assumptions remain explicitly visible in the UI and documentation, and automated regression tests remain required. Any expansion into patient-specific, prescribing, dispensing, payer, pharmacy-workflow, or clinical-decision use reopens the review requirement.

## Administrative actions

The following settings are repository or platform administration actions and are not satisfied merely by committing code:

- set repository visibility to private;
- permit and enable pull-request auto-merge;
- require CI, CodeQL, and dependency-review checks for `main`;
- enable dependency graph, Dependabot alerts, and secret scanning where supported;
- restrict deployment to the approved internal/intranet environment.

## Status language

These decisions authorize continued engineering and internal evaluation. They do not establish HIPAA, HITRUST, SOC 2, FedRAMP, medical-device, clinical-validation, or other compliance status.
