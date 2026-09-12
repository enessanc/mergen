# ADR 0001: Preserve private repository despite unavailable GitHub branch protection

- Status: Accepted
- Date: 2026-09-12
- Phase: 0
- Decision owner: Repository maintainer

## Context

Mergen requires Git review and explicit human approval before promotion into
integration, QA, or release branches. The desired GitHub protections for
`main`, `dev-user`, and `dev-agent` require pull requests, one approval,
stale-review dismissal, and force-push/deletion prohibition.

On 2026-09-12, GitHub's branch-protection API returned HTTP 403 for the private
`enessanc/mergen` repository: the current account plan does not support this
feature for private repositories.

## Decision

Keep `enessanc/mergen` private. Apply the branch-promotion and human-review
rules procedurally through `AGENTS.md` and `docs/development-workflow.md`.
Do not give any agent credential direct write authority to `dev-agent`,
`dev-user`, or `main`. Re-evaluate and enable technical branch protection
before Phase C authorizes an automated control plane, or earlier if the account
plan/visibility changes.

## Consequences

The Git host does not presently enforce PR-only promotion; the human maintainer
must enforce it. This is an acknowledged Phase 0 governance limitation, not a
security exception for agent workloads. The repository remains private, which
is preferred while architecture and operating details are still developing.

## Verification

Record a successful branch-protection API/configuration check in the relevant
Phase C entry evidence before automated execution is authorized.
