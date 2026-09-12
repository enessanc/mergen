# ADR 0002: Use a public repository with protected human promotion branches

- Status: Accepted
- Date: 2026-09-12
- Phase: 0
- Decision owner: Repository maintainer

## Context

The current GitHub account cannot enable branch protection on the private
repository. Mergen is intended to be open source, and its architecture and
planning files contain no secrets or deployment credentials. The maintainer
needs `dev-user` as the leading branch, a separate agent integration path, and
technical prevention of direct updates to human promotion and release branches.

## Decision

`enessanc/mergen` is public and has `dev-user` as its default branch. GitHub
protects `dev-user` and `main` with PR-only updates, admin enforcement,
conversation resolution, stale-review dismissal, no force push, and no branch
deletion. Required approval count is zero for the single-account workflow.

An agent synchronizes `dev-agent` from `dev-user` before each task, locally
merges its completed feature branches into `dev-agent`, pushes that integration
branch, and deletes completed feature branches locally and remotely. It opens
one phase PR from `dev-agent` to `dev-user`; the maintainer alone merges it.
Only a maintainer promotes `dev-user` to `main` for a release.

## Consequences

Repository contents must remain suitable for public disclosure. GitHub
technically blocks direct updates to `dev-user` and `main`; it deliberately
does not block the agent's integration work on `dev-agent`. The required
approval count cannot distinguish a human action from the account token, so
the maintainer must review the PR before merging it.

## Verification

Confirm repository visibility/default branch and inspect protection settings for
`dev-user` and `main`. Confirm `dev-agent` remains unprotected. For each task,
record the sync, feature deletion, validation, and phase PR in its evidence.
