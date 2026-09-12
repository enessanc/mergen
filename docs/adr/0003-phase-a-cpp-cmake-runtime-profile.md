# ADR 0003: Use an Ubuntu 22.04 non-root C++/CMake runtime proof

- Status: Accepted
- Date: 2026-09-12
- Phase: A
- Decision owner: Repository maintainer

## Context

Phase A needs a small reproducible disposable runtime before Mergen controls
Docker or Kubernetes. The design baseline recommends C++/CMake as the first
profile. The host currently provides CMake 3.22 and GCC 11, while no container
runtime is installed for local execution.

## Decision

Use `ubuntu:22.04` as the initial profile base. Install only CMake, Ninja,
build-essential, Git, and CA certificates. The image executes the validation
entrypoint as UID/GID `10001`; it configures, builds, and tests a mounted CMake
project in `/tmp/mergen-build`.

The proof command uses a read-only project mount, read-only root filesystem,
tmpfs build directory, no network, dropped capabilities, no-new-privileges,
PID/CPU/memory limits, and no host or Docker-socket mount.

## Consequences

The proof demonstrates a safe baseline but is intentionally generic: it is not
yet a versioned `.mergen/project.yaml` contract or a Kubernetes Job. A GitHub
Actions workflow runs the documented hardened container commands on every
`dev-agent` push and `dev-user` PR because a Docker-compatible runtime is not
available to the current user.

## Verification

Run the success and intentional-failure commands in
`infrastructure/docker/README.md` locally when Docker becomes available. Until
then, record the GitHub Actions run URL, commands, outcome, and source-tree
check in the Phase A evidence record.
