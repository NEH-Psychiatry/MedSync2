# Security Policy

## Reporting a vulnerability

Do not disclose a suspected vulnerability in a public issue. Use GitHub's private security-advisory workflow for this repository and include:

- affected file or workflow;
- reproduction steps;
- expected and observed behavior;
- potential impact;
- any known mitigation.

## Current security boundary

The application is a calculation-only Streamlit interface. The repository does not currently implement authentication, authorization, a database, an API, audit logging, or a managed-secret integration.

The owner-approved current posture is private-repository, internal/intranet use with synthetic or non-identifiable entries only. This posture does not authorize protected or identifiable patient data and does not convert repository privacy into application access control.

A hosted Streamlit session transmits values between the user's browser and the application server even when the code does not intentionally persist them. Public internet exposure is outside the approved current posture.

## Data-handling rules

- Do not enter patient names, dates of birth, medical-record numbers, addresses, or other identifiers.
- Do not log medication entries or calculation results.
- Do not commit secrets, credentials, tenant identifiers, subscription identifiers, or patient data.
- Treat screenshots, exported results, and server logs as potentially sensitive.
- Use synthetic or non-identifiable examples only.
- Restrict access to approved internal users through an approved internal network path and TLS.

## Clinical-use boundary

The application is not a prescribing, dispensing, medication-ordering, pharmacy-workflow, payer, or clinical-decision system. The owner has not required a separate external clinical/pharmacy review for the current internal, calculation-only use case. Any expansion beyond that scope reopens the review and control requirements.

## Controls required before identifiable-data use

Before handling regulated or identifiable health information, document and approve at least:

- authentication and least-privilege authorization;
- HTTPS/TLS termination;
- network exposure and ingress controls;
- managed secret storage and rotation;
- logging, retention, and redaction rules;
- incident response and vulnerability-management ownership;
- backup and recovery requirements, if persistence is added;
- vendor agreements and compliance scope appropriate to the deployment.

## Repository administration

The owner-approved target settings are:

- private repository visibility;
- required CI, CodeQL, and dependency-review checks on `main`;
- automatic pull-request merge only after required checks pass;
- dependency graph, Dependabot alerts, and secret scanning enabled where supported.

These are GitHub administration settings and must be verified separately from the code diff.

No compliance certification, regulated-data authorization, clinical-validation claim, or regulatory suitability is established by this repository.
