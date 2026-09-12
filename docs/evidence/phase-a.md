# Phase A verification record

- Status: In progress — awaiting GitHub Actions container verification
- Date: 2026-09-12
- Reviewer: Pending
- Environment and versions: Ubuntu 22.04 host; CMake 3.22.1; GCC 11.4.0;
  Docker/K3s/kubectl unavailable at record creation.
- Related ADRs: ADR 0003

## Objective and scope

Provide a reproducible, non-root C++/CMake runtime image and demonstrate its
success and failure behavior without adding Kubernetes, Plane, or Mergen Core.

## Procedure and commands

The image-build and run commands are versioned in
`infrastructure/docker/README.md`.

## Successful-path evidence

The CMake fixture configures, builds, and passes natively on the host. The
`Phase A runtime proof` GitHub Actions workflow will perform the same proof in
a real Docker runner because no Docker-compatible runtime is installed or
reachable by the current user.

The first workflow run (`34699462297`) built the image and passed the non-root
and socket checks, but CTest could not execute its binary from the runner tmpfs.
The run command now explicitly requests an executable tmpfs; the replacement
workflow run is the required final evidence.

## Intentional failure-path evidence

The fixture returns failure when `MERGEN_PROOF_FAIL=1`. The workflow asserts
the same non-zero Docker exit behavior.

## Security and privilege checks

The Dockerfile declares an unprivileged UID/GID. The documented run command
uses a read-only root and source mount, tmpfs build directory, no network,
dropped capabilities, no-new-privileges, PID/CPU/memory limits, and no Docker
socket/host mount. The workflow verifies UID and socket absence at runtime.

## Persistent and ephemeral state

Fixture source is read-only. Build output is `/tmp/mergen-build` in the
container tmpfs and is destroyed with the container.

## Known limitations and next gate

Phase A cannot pass until the workflow captures successful and intentional
failure container exits. A manual local run remains pending Docker access. Do
not begin Phase B until the workflow result is recorded.
