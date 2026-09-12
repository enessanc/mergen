# Development, validation, and promotion workflow

## Origin and adaptation

This procedure adapts the workflow documented in the `enessanc/sentio`
repository: documentation-first context, dependency-ordered planning, focused
branches, Conventional Commits, and mandatory validation before commit. Mergen
uses `dev-user` as the leading human branch while retaining a separate
agent-integration branch.

`AGENTS.md` is the normative concise protocol. This document explains how to
apply it and should evolve only through an approved ADR when the process changes.

## Work-item lifecycle

```text
Approved phase and work item
  → merge current dev-user into dev-agent
  → agent/<work-item>-<slug> from dev-agent
  → implementation + deterministic validation
  → evidence record + focused Conventional Commit(s)
  → local feature merge into dev-agent + push
  → delete local and remote feature branch
  → phase PR from dev-agent to dev-user
  → human review and merge to dev-user
  → PR to main for release
  → human review, merge, and release tag
```

An agent may locally merge a verified feature branch into `dev-agent` and push
that branch. No agent may merge a PR into `dev-user` or `main`. The Mergen
product's later Plane-to-Git automation follows the same principle: it creates
a review branch and reports validation, while a human controls promotion.

## Required PR description

Use this checklist in every PR body:

```md
## Scope
- Phase/work item:
- What changed:
- Explicit non-goals:

## Validation
- [ ] Format: `<command and result>`
- [ ] Static analysis/type check: `<command and result>`
- [ ] Unit tests: `<command and result>`
- [ ] Integration or real-path check: `<command and result, if applicable>`
- [ ] Intentional failure check: `<procedure and result, if applicable>`

## Risk and governance
- Security/privilege/network impact:
- Persistent-state or migration impact:
- Linked ADR/evidence/runbook:
- Known limitations and rollback:
```

The exact commands are versioned in `.mergen/project.yaml` after the project
contract is introduced. Until then, the phase evidence record names the manual
commands used.

## Branch protection baseline

The public repository's default branch is `dev-user`. GitHub protects
`dev-user` and `main` with pull-request-only updates, required conversation
resolution, stale-review dismissal, no force push, no deletion, and admin
enforcement. Required review count is zero: the human maintainer's intentional
PR merge supplies the approval boundary in this single-account workflow.

`dev-agent` is intentionally unprotected so an agent can merge its task branch
locally and push the completed integration work. Before every task, it must
incorporate remote `dev-user` into `dev-agent`; unresolved conflicts require
maintainer direction. See ADR 0002.

## Commit rules

- Prefer Conventional Commit types: `feat`, `fix`, `docs`, `test`, `refactor`,
  `build`, `ci`, `chore`, and `security`.
- Do not amend, rebase published work, reset hard, force-push, or use
  destructive checkout unless a human maintainer explicitly directs it.
- Do not commit secrets or local runtime output. Use repository ignore rules as
  soon as a runtime can produce them.
