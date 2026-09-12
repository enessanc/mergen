# Mergen contributor guide

## Purpose and source of truth

Mergen is a self-hosted, remote-first personal AI engineering orchestration
platform. It turns a Plane work item into a policy-controlled, disposable agent
execution and returns a reviewable Git result. Human Git review and explicit
approval are the acceptance boundary.

The current architectural baselines are:

- `doc/Mergen_System_Design_Description_Rev2.0.docx` (`MERGEN-SYS-DES-001`)
- `doc/Mergen_System_Implementation_Plan_Rev2.0.docx` (`MERGEN-SYS-IMP-001`)
- `PLANS.md`, which operationalizes those baselines for this repository.

When documents disagree, stop and record the discrepancy in a decision record;
do not silently choose an implementation direction.

## Working agreement

1. Work one approved phase at a time. Satisfy its exit criteria and record
   evidence before starting the next phase.
2. Complete one small manual exercise for each new infrastructure primitive
   before automating that primitive in Mergen.
3. Keep the initial control plane a Python modular monolith. Preserve explicit
   boundaries for Runner, Project Contract, Git, Plane, Model Gateway, Policy,
   and Event Store.
4. Prefer real-path verification over mocks for infrastructure behavior.
   Deterministic domain logic must still have automated unit tests.
5. Keep persistent execution state and semantic events outside disposable Pods.
   A Pod workspace is ephemeral and is never the sole copy of important state.
6. Update relevant documentation, acceptance evidence, and decision records in
   the same change as an approved behavior or interface change.

## Non-negotiable security invariants

- Agent Pods are untrusted and must use least privilege.
- Never provide agents with Kubernetes control credentials, Docker socket,
  host filesystem mounts, host networking, host PID/IPC, or privileged mode.
- Run agent workloads non-root with dropped capabilities, resource limits, and
  execution timeouts.
- Default to explicitly scoped network access; do not introduce broad egress
  without a documented, approved need.
- Keep Plane, Git, and model-provider credentials in trusted integrations or
  narrowly scoped mechanisms; never inject broad credentials into a Pod.
- Agents must not force-push or update protected base branches directly.
- Required deterministic validation decides success. An agent statement alone
  can never mark an execution successful.

## Repository conventions

- `docs/adr/`: short Architecture Decision Records; use the template there.
- `docs/evidence/`: phase verification records and links to reproducible logs.
- `docs/runbooks/`: operator procedures written only after the related proof.
- `contracts/`: versioned public/project/API/event contracts once their phase is
  approved. Do not publish speculative contracts as stable.
- `infrastructure/`: manually exercised Docker and Kubernetes artifacts, added
  only in Phases A and B respectively.
- `src/` and `tests/`: application code and tests, intentionally empty until
  Phase C is authorized.

## Development and Git workflow

This workflow adapts the proven Sentio approach to Mergen's stronger
human-acceptance boundary. It governs both human contributors and coding agents.

### Branch roles

| Branch | Purpose | Who may merge into it |
| --- | --- | --- |
| `main` | announced, stable releases | human maintainer only |
| `dev-user` | human QA/staging and release-candidate integration | human maintainer only |
| `dev-agent` | reviewed integration of agent-produced work | human maintainer only |
| `agent/<work-item>-<slug>` | one isolated implementation task | never a merge target |

Create every task branch from the current `dev-agent`. An agent may commit and
push its own task branch and open a pull request into `dev-agent` only when that
operation has been explicitly authorized for the task. It must never commit,
push, merge, or force-push `dev-agent`, `dev-user`, or `main` directly.

The expected promotion path is:

`agent/<work-item>-<slug> → PR → dev-agent → human-reviewed PR → dev-user → human-reviewed PR → main`

The temporary exception in Sentio that allowed agents to merge into its agent
integration branch is intentionally **not** adopted. It would conflict with
Mergen's system baseline: Git review and explicit human approval are the final
acceptance boundary.

### Task procedure

1. Read the authoritative system documents, `PLANS.md`, relevant ADRs, project
   contract, and existing evidence before changing anything.
2. Confirm the work belongs to the currently approved phase. Record a new ADR
   before choosing a consequential architecture, security, persistence, or
   external-interface direction.
3. Create one task branch with its work-item identifier. Keep the change small
   and scoped; do not combine unrelated refactors.
4. Implement the task and its deterministic tests together. Run the phase's
   prescribed validation, including a relevant intentional failure check where
   practical.
5. Update `PLANS.md`, the evidence record, runbook, and contracts when the
   task changes their stated behavior.
6. Format, lint/type-check, test, and review the diff before committing. The
   project contract will define the exact commands once Phase A establishes a
   runtime; until then, do not invent tool-specific checks.
7. Commit only verified work using Conventional Commits, for example
   `docs(phase-0): define Git promotion workflow` or
   `feat(runner): create Kubernetes Job manifest`. Separate unrelated code,
   tests, and documentation into logical commits when feasible.
8. Push only the task branch and open a PR with scope, validation commands and
   results, failure-path evidence, security impact, linked work item/ADR, and
   known limitations. A maintainer performs review and every merge.

### Pull-request gate

A PR must not be merged unless all applicable requirements are satisfied:

- The PR has a single approved phase/task scope and a clear rollback path.
- Required formatting, static analysis, unit tests, and integration/real-path
  checks pass; intentionally failed checks are recorded where required.
- Deterministic validation output is attached or reproducibly linked.
- No secret, generated workspace, credential, kubeconfig, or unsafe privilege
  change is included.
- Branch target and protection rules are correct; the PR never bypasses review.
- Documentation, evidence, and ADRs reflect the resulting behavior.

For Mergen Alpha executions, the system's task branch is a review artifact, not
permission to merge. Validation failure must leave the work item out of a
successful review state and prevent any promotion.

Use clear, narrowly scoped commits. Do not mix phase work with unrelated
refactoring. Never commit secrets, kubeconfigs, provider tokens, private keys,
or generated runtime workspaces.

## Phase handoff rule

Before requesting the next phase, add an evidence record stating: objective,
environment/version, commands or manual procedure, successful result, an
intentional failure result, security checks, known limitations, and the
reviewer/date. Link it from `PLANS.md`'s phase ledger or the phase PR.

## Current status

Planning foundation only. No implementation phase is authorized by this
repository baseline yet. The next authorized activity is Phase 0 in `PLANS.md`:
confirm the operating assumptions and record its decisions. Phase A begins only
after that gate is passed.
