# Phase A verification record

- Status: Passed — real Docker validation completed in GitHub Actions
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

The CMake fixture configures, builds, and passes natively on the host. GitHub
Actions run `34699540062` completed successfully in a real Docker runner:
https://github.com/enessanc/mergen/actions/runs/34699540062

The run built the image, verified its UID and socket absence, ran the fixture
with CPU/memory/PID limits, and completed CTest successfully. An earlier run
(`34699462297`) exposed an executable-tmpfs issue; it was fixed by explicitly
requesting `exec` and the successful replacement run is the final evidence.

## Intentional failure-path evidence

The fixture returns failure when `MERGEN_PROOF_FAIL=1`. The successful workflow
run asserts the Docker command returns non-zero for that case.

## Security and privilege checks

The Dockerfile declares an unprivileged UID/GID. The documented run command
uses a read-only root and source mount, tmpfs build directory, no network,
dropped capabilities, no-new-privileges, PID/CPU/memory limits, and no Docker
socket/host mount. The workflow verifies UID and socket absence at runtime.

## Persistent and ephemeral state

Fixture source is read-only. Build output is `/tmp/mergen-build` in the
container tmpfs and is destroyed with the container.

## Known limitations and next gate

Phase A exit criteria are met through the real Docker workflow. A manual local
run remains a useful learning exercise when Docker access becomes available,
but it is not a blocker. Phase B requires a reachable K3s/Kubernetes cluster.
