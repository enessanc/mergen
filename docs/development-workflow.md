# Development, validation, and promotion workflow

## Origin and adaptation

This procedure adapts the workflow documented in the private `enessanc/sentio`
repository: documentation-first context, dependency-ordered planning, focused
branches, Conventional Commits, and mandatory validation before commit. Mergen
retains those practices but requires human approval at every merge boundary to
honor its system-level Git acceptance rule.

`AGENTS.md` is the normative concise protocol. This document explains how to
apply it and should evolve only through an approved ADR when the process changes.

## Work-item lifecycle

```text
Approved phase and work item
  → agent/<work-item>-<slug>
  → implementation + deterministic validation
  → evidence record + focused Conventional Commit(s)
  → PR to dev-agent
  → human review and merge
  → PR to dev-user for QA
  → human review and merge
  → PR to main for release
  → human review, merge, and release tag
```

No agent may merge any of these pull requests. The Mergen product's later
Plane-to-Git automation follows the same principle: it creates a review branch
and reports validation, while a human controls promotion.

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

The desired configuration for `main`, `dev-user`, and `dev-agent` is: require
pull requests, at least one human approval, up-to-date required checks once CI
exists, no force pushes, and no direct deletion. Configure the same protection
semantically if another Git provider is later used.

At repository bootstrap, GitHub rejected this configuration for the private
repository because the current account plan does not support private-repository
branch protection. Until the account plan or repository visibility changes, the
rules in `AGENTS.md` are mandatory procedural controls and only the human
maintainer's GitHub credential may have write access. See ADR 0001. Re-attempt
technical protection before authorizing automated execution in Phase C.

## Commit rules

- Prefer Conventional Commit types: `feat`, `fix`, `docs`, `test`, `refactor`,
  `build`, `ci`, `chore`, and `security`.
- Do not amend, rebase published work, reset hard, force-push, or use
  destructive checkout unless a human maintainer explicitly directs it.
- Do not commit secrets or local runtime output. Use repository ignore rules as
  soon as a runtime can produce them.
