# Container deployment baseline

Status: executable development and controlled internal-evaluation artifact; not
an approved production deployment.

This record documents the assumptions introduced by the repository
`Dockerfile` and links them to the cloud-adoption backlog. It accepts a
repeatable container build for validation without selecting a cloud platform
or authorizing regulated-data use.

## Security assumptions

- The image runs as a non-root user and exposes only the Streamlit port.
- The container does not supply authentication, authorization, TLS, a web
  application firewall, rate limiting, tenant isolation, or secret management.
- Deployment must use an approved private network path and an authenticated TLS
  ingress. No production secret may be baked into the image or supplied in a
  committed environment file.
- Base image provenance, vulnerability scanning, signature/attestation,
  registry access, patch cadence, and runtime policy remain deployment-owner
  responsibilities.
- Until those controls are evidenced, use is limited to a developer workstation
  or controlled internal evaluation with synthetic or non-identifiable data.

## Cost assumptions

- A local developer run has no separately budgeted cloud-runtime cost.
- Cloud compute, registry, ingress, logging, monitoring, egress, backup,
  support, and security-service costs are **not applicable to this baseline**
  because no production platform or service tier has been selected.
- Before any shared or production-like deployment, complete
  [P1-3: cost-management and FinOps plan](../cloud-adoption-backlog.md#p1-3-add-cost-management-and-finops-plan)
  with a named cost owner, environment estimates, budget alerts, review
  cadence, and shutdown/decommission behavior.

## Reliability assumptions

- The image is a single Streamlit process with a health check. It provides no
  high availability, autoscaling, queueing, failover, disaster recovery, or
  zero-downtime deployment guarantee.
- The application intentionally has no persistent store, so application-level
  backup and restore are not applicable. Platform configuration, image,
  registry, audit, and log recovery still require an owner decision.
- No SLO, capacity target, recovery-time objective, or recovery-point objective
  has been approved. Shared or production-like use is blocked until those are
  documented and tested.

## Data assumptions

- Only synthetic or non-identifiable input is approved.
- Browser-to-server values can appear in platform, proxy, exception, access, or
  observability logs even though the application does not intentionally
  persist entries.
- PHI, patient identifiers, medication-order data, and production records are
  prohibited until data classification, logging/redaction, retention,
  deletion, access-control, incident-response, and vendor/BAA decisions are
  approved.

## Compliance assumptions

- This artifact establishes no HIPAA, HITRUST, SOC 2, FedRAMP, medical-device,
  clinical-validation, prescribing, dispensing, or pharmacy-workflow status.
- A production-like deployment requires the release checklist, security and
  privacy review, data-protection decision, compliance evidence owner, and any
  applicable clinical/pharmacy review.

## Backlog linkage and exit gate

The container is the local execution input to
[P1-1: deployment topology](../cloud-adoption-backlog.md#p1-1-build-medsync2-deployment-topology).
It does not complete that item. P0 identity/environment, repository, architecture,
and regulated-data decisions must be complete or formally accepted by named
owners before P1 deployment work proceeds.

Production deployment remains blocked until the deployment topology,
cost-management plan, protected environment, approved visibility, data
boundary, security controls, observability, recovery evidence, and named
release approval are complete.
