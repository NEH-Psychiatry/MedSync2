# Identity and Access Decision Record

Status: draft

Date: 2026-10-07

## Decision

MedSync2 has not yet selected a final identity and access model. This record defines the minimum decision fields that must be completed before any authentication, authorization, or deployment credential is implemented. No hard-coded credentials are permitted; access must be expressed through managed identity, federated workload identity, or a managed secret store. [MedSync2 decision]

## Context

The Azure Essentials operating model treats identity as a readiness-and-foundation prerequisite: environments, deployments, and data access all depend on a defined identity provider, role model, and credential-handling approach. For MedSync2, identity decisions also intersect with regulated-data posture (PHI/PII access, audit logging), so they must be made before persistent data stores or external integrations are connected. [Azure Essentials]

Current Microsoft terminology: Microsoft Entra ID (formerly Azure Active Directory / Azure AD). Verify current naming, roles, and federation paths against Microsoft documentation before implementation. [MSFT docs: https://learn.microsoft.com/en-us/entra/fundamentals/new-name]

## Required decisions

| Area | Current answer | Owner | Status |
|---|---|---|---|
| Identity provider | Microsoft Entra ID assumed for Azure-native identity | To be assigned | Draft assumption |
| Human user model | To be determined (users, groups, directory source) | To be assigned | Open |
| Service and automation identities | Managed identities preferred over secrets; specifics to be determined | To be assigned | Open |
| Break-glass access | Emergency-access account policy required but not defined | To be assigned | Open |
| Role model | Least-privilege roles required; concrete role-to-scope mapping to be determined | To be assigned | Open |
| GitHub-to-Azure authentication | OIDC workload-identity federation preferred over long-lived secrets; to be confirmed | To be assigned | Open |
| GitHub secrets and environments | Which environments require approvals and which secrets are stored where | To be assigned | Open |
| Production access workflow | Approval, just-in-time, and audit approach to be determined | To be assigned | Open |
| Credential rotation | Rotation ownership and cadence to be determined | To be assigned | Open |
| Access audit logging | Sign-in and authorization audit source and retention to be determined | To be assigned | Open |

## Principles

- No hard-coded credentials, tenant IDs, subscription IDs, API keys, or patient identifiers in source, configuration, tests, or documentation. [MedSync2 decision]
- Prefer managed identity and OIDC workload-identity federation over long-lived secrets. Use a managed secret store (for example Azure Key Vault) only where a secret is unavoidable. [Azure Essentials]
- Apply least privilege: grant the narrowest role at the narrowest scope that satisfies the task. [Azure Essentials]
- Separate human, service, automation, and break-glass identities; do not reuse one identity across these categories. [MedSync2 decision]

## Options to evaluate

### Option A: OIDC workload-identity federation for CI/CD plus managed identities for runtime

GitHub Actions authenticates to Azure using OIDC federation (no stored cloud secrets), and the MedSync2 runtime uses managed identities for Azure resource access.

Best fit when:

- Deployments run from GitHub Actions.
- The team wants to minimize stored secrets.

Risks:

- Requires correct federation and trust configuration.
- Role scoping must be reviewed to avoid over-permissioning.

### Option B: Managed secret store with service principals

Use service principals with credentials stored in a managed secret store for environments where OIDC federation is not available.

Best fit when:

- An integration or environment cannot use managed identity or OIDC.

Risks:

- Introduces secrets that must be rotated and audited.
- Higher operational burden and larger attack surface.

### Option C: Defer identity implementation

Keep identity assumptions documented but implement no authentication or credential flow until deployment topology and data classification are decided.

Best fit when:

- Application architecture and regulated-data posture are still unresolved.

Risks:

- Identity controls may be rushed when deployment becomes planned.

## Recommended next step

1. Confirm the Azure tenant and subscription strategy (see the Azure landing-zone decision record).
2. Decide the GitHub-to-Azure authentication path (Option A preferred).
3. Define the least-privilege role model and break-glass policy.
4. Complete the data-protection decision record, which depends on the access and audit model defined here.

## Decision outcome

Pending.

## Review cadence

Review this record whenever one of the following changes:

- New environment or deployment path is added.
- Production deployment becomes planned.
- PHI, PII, or regulated workflow assumptions change.
- A new external integration requires authentication.
- AI or agent functionality that needs identity is introduced.
