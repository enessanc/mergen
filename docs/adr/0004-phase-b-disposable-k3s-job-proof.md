# ADR 0004: Verify the Kubernetes execution primitive with disposable K3s Jobs

- Status: Accepted
- Date: 2026-09-12
- Phase: B

Phase B uses a single-node K3d/K3s CI cluster because no local K3s exists. The
proof image contains only the CMake fixture; jobs receive no host mount,
registry credential, or Kubernetes API token. Success, validation failure, and
deadline failure are separate Jobs so terminal outcomes are unambiguous. The
manifest is a proof primitive, not Mergen Core or its eventual runner API.
