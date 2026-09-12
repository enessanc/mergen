# ADR 0001: Preserve private repository despite unavailable GitHub branch protection

- Status: Superseded by ADR 0002
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

This historical decision was superseded when the repository was made public and
GitHub branch protection became available. ADR 0002 records the replacement.
