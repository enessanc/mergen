# Phase B: K3s Job proof

`runtime-proof/` contains a namespace, tokenless service account, default-deny
network policy, and three hardened Jobs. They prove successful execution,
validation failure, and deadline expiry. The Jobs use a non-root security
context, read-only root filesystem, `emptyDir` tmpfs, dropped capabilities,
resource limits, `activeDeadlineSeconds`, and TTL cleanup.

The GitHub `Phase B K3s Job proof` workflow creates a disposable single-node
K3s cluster with K3d v5.9.0, imports the image without a registry or hostPath,
then verifies all three lifecycle paths. A local K3s cluster is required before
these manifests may be used outside CI.
