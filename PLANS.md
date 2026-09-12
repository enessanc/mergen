# Mergen implementation procedure

## Status

This is the execution procedure for the Revision 2.0 system baseline. It is a
gated plan, not an authorization to implement every phase. Current state:
**Phase 0 — planning foundation**. No application, runtime, Kubernetes, or
external-service implementation has started.

## Target Alpha outcome

An authorized Plane work item moves through this deterministic path:

`Ready for Agent → policy/project validation → disposable Kubernetes Job → scoped repository task branch → deterministic validation → pushed review branch → Plane In Review → cleanup`

Alpha is accepted only after this works repeatedly against a real repository,
including an intentional failure path, without exposing Kubernetes credentials,
the host filesystem, or the Docker socket to the agent workload.

## Governance and evidence

Every phase has four gates:

1. **Entry:** prerequisites, assumptions, scope, and interfaces are documented.
2. **Build:** only the stated deliverables are changed.
3. **Verification:** real-path success and deliberate failure behavior are
   demonstrated; deterministic logic has appropriate automated tests.
4. **Exit:** evidence, security checks, known limitations, and an ADR for a
   consequential decision are reviewed and recorded.

Use `docs/evidence/phase-<id>.md` for evidence and `docs/adr/NNNN-title.md` for
decisions. A phase cannot advance on a passing happy path alone.

## Phase 0 — planning foundation (current)

**Objective:** turn the system baseline into an executable, reviewable work
program without selecting implementation details prematurely.

**Deliverables:**

- This plan, `AGENTS.md`, repository layout, ADR template, and evidence template.
- An agreed execution environment inventory: host OS, Docker availability,
  K3s choice, private-management/WireGuard boundary, Git provider, Plane
  deployment/API version, and model/package endpoint requirements.
- A named first dogfood repository and a deliberately harmless task suitable
  for later validation.
- Initial decisions for Python version, dependency management, database
  migration approach, container registry, secret-storage approach, and CI
  posture. Record decisions—not guesses—in ADRs.

**Exit checks:** assumptions are confirmed; unknowns and owners are visible;
Phase A's selected repository/runtime is approved; no secrets or environment
credentials are present in the repository.

## Phase A — Docker runtime proof

**Objective:** prove a reproducible, disposable project runtime manually.

**Deliverables:** one minimal runtime image (prefer C++/CMake first), a hardened
baseline Dockerfile pattern, a documented manual build/test command, and a
record of explicit inputs/outputs for later automation.

**Verification:** run from a clean checkout without a host toolchain; verify
unambiguous success and intentionally failing exit states; apply CPU/memory
limits; run non-root; confirm no privileged mode or Docker socket is needed.

**Exit:** destroying and recreating the container loses no required source
state. Do not add Kubernetes, Plane, or custom UI work in this phase.

**Evidence:** [Phase A verification record](docs/evidence/phase-a.md) — passed.

## Phase B — Kubernetes/K3s Job proof

**Objective:** represent the proven runtime as a disposable Kubernetes Job.

**Deliverables:** single-node K3s environment, manual Job manifest, job
status/log inspection procedure, cleanup procedure, explicit configuration
passing, limits, hardened security context, and minimal service-account/RBAC
model.

**Verification:** demonstrate successful, failing, and timed-out Jobs; inspect
their status/logs; verify cleanup; confirm no hostPath, Docker socket, or Pod
Kubernetes administrative credential is required.

**Exit:** an entire disposable task is represented by Job/Pod lifecycle. Do not
introduce Helm, operators, service mesh, or production multi-node scope.

**Evidence:** [Phase B verification record](docs/evidence/phase-b.md) — passed.

## Phase C — Mergen Core skeleton

**Objective:** build the deterministic Python control plane around the proven
Job model.

**Deliverables:** modular-monolith package layout; FastAPI/Pydantic API;
execution entity and explicit state machine; persistent execution/event data;
Runner interface and KubernetesRunner; create/get/stop surface; controller
restart reconciliation.

**Verification:** unit-test legal and illegal transitions; use the API to
launch/observe a real Job; restart the controller and reconcile active and
completed executions.

**Exit:** Core creates, observes, terminates, and records one real execution
deterministically. Defer routing, rich events, checkpointing, and frontend.

## Phase D — Git and deterministic validation lifecycle

**Objective:** make execution produce an auditable reviewable code change.

**Deliverables:** task-branch convention; scoped checkout/clone; configured
validation runner; commit/push lifecycle; stored branch, commit, validation
summary, and failure metadata.

**Verification:** use a temporary or designated test repository; prove base
branch protection; make a test intentionally fail; prove success produces a
reviewable branch.

**Exit:** a real repository task reaches a reviewable Git result through the
Kubernetes path. Automated merge and force push remain out of scope.

## Phase E — Plane integration

**Objective:** use Plane as Alpha's remote task and workflow interface.

**Deliverables:** one explicit trigger (such as `Ready for Agent`), idempotent
work-item-to-execution mapping, controlled metadata mapping, and running/result
status synchronization.

**Verification:** duplicate webhook delivery creates exactly one execution;
Plane outage does not corrupt Mergen state; success moves/comments to `In
Review`; failure reports diagnostics without claiming success.

**Exit:** the Alpha path can be initiated remotely from Plane. No Plane fork or
custom Mergen UI is added.

## Phase F — minimum security baseline and Alpha stabilization

**Objective:** make the proven path safe enough for routine homelab dogfooding.

**Deliverables:** explicit Pod security baseline; scoped Core-to-Kubernetes
privileges; timeout and cleanup policy; minimal audit events; Alpha runbook and
known-limitations document.

**Verification:** negative-test at least one prohibited policy/privilege;
verify no agent host/infrastructure access; verify failed and timed-out tasks
reach terminal states and are cleaned up; repeat end-to-end Alpha runs.

**Exit:** the Alpha release gate passes repeatedly, is tagged/documented, and
is ready for dogfooding.

## Post-Alpha order

Proceed only when the prior capability has evidence and a real demand:

| Order | Capability |
| --- | --- |
| G | Project Contract and Project Registry |
| H | Semantic Event Model and Intervention API (REST/SSE) |
| I | Token and Resource Manager |
| J | Advanced security hardening |
| K | TSNL dogfood |
| L | Umay dogfood |
| M | Model Gateway and Router |
| N | Sentio dogfood |
| O | Observability and artifact management |
| P | Independent Mergen Web/PWA |
| Q | Bootstrap/onboarding agent |
| R | Leader dogfood |
| S | Mergen 1.0 stabilization |

## Cross-phase acceptance checklist

- [ ] Scope and non-goals stayed within the phase.
- [ ] Manual learning exercise completed for new core primitives.
- [ ] Happy path works against the appropriate real environment.
- [ ] At least one relevant failure path was deliberately exercised.
- [ ] Persistent versus ephemeral state is explicit.
- [ ] Security assumptions, privileges, secrets, and network access are documented.
- [ ] Deterministic domain/configuration logic has automated tests where practical.
- [ ] ADRs, runbooks, and evidence are updated.
- [ ] Known limitations and the next gate are recorded.

## Explicit deferrals through Alpha

Custom Web/PWA and TypeScript/React UI; graphical live timelines; checkpoint or
rewind UX; token-aware scheduling and advanced routing; multi-agent roles;
full observability stack; artifact store; and advanced network-policy profiles.
