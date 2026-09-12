# Mergen

Planning-first repository for Mergen, a self-hosted personal AI engineering
orchestration platform.

No product implementation is present yet. Read [PLANS.md](PLANS.md) for the
gated procedure and [AGENTS.md](AGENTS.md) for contributor and security rules.
The authoritative Revision 2.0 source documents are retained in `doc/`.
The adopted branch, validation, and PR procedure is described in
[`docs/development-workflow.md`](docs/development-workflow.md).

## Initial layout

```
contracts/       future versioned contracts
docs/adr/        architecture decisions
docs/evidence/   phase verification records
docs/runbooks/   operating procedures proven by a phase
infrastructure/  Docker and Kubernetes artifacts when their phases begin
src/             application source, reserved for Phase C
tests/           tests, reserved for Phase C
```

The next activity is Phase 0 planning confirmation; do not implement runtime
or application components until its entry and exit checks are satisfied.
