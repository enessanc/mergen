# Phase A: C++/CMake runtime proof

This is the first disposable runtime proof, not Mergen application code. The
image builds and validates a mounted CMake project as an unprivileged user. The
source mount is read-only and the build directory lives under the container's
ephemeral `/tmp` filesystem.

## Build the image

From the repository root:

```bash
docker build --tag mergen/cpp-cmake:0.1 infrastructure/docker/cpp-cmake
```

## Successful validation

```bash
docker run --rm --init \
  --user 10001:10001 \
  --read-only \
  --tmpfs /tmp:rw,nosuid,nodev,size=512m \
  --network none \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --pids-limit 256 \
  --cpus 2 \
  --memory 4g \
  --volume "$(pwd)/infrastructure/docker/proof-project:/workspace:ro" \
  mergen/cpp-cmake:0.1
```

Expected result: CMake configures and builds the fixture, `ctest` passes, and
the command exits with status `0`.

## Intentional failure validation

Use the same command with `--env MERGEN_PROOF_FAIL=1` before the image name.
`ctest` must report the intentional test failure and Docker must return a
non-zero exit status.

## Security and lifecycle assertions

- The runtime image executes as UID/GID `10001`, not root.
- It has no Docker socket, host mount, privileged mode, capabilities, network,
  or Kubernetes credential.
- The fixture source is read-only; the build output is in an ephemeral tmpfs.
- Removing the container removes the build workspace. The source checkout is
  unchanged by either validation command.
