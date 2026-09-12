# Homelab bootstrap

Prerequisites: a private Linux host, Docker-compatible runtime, K3s, `kubectl`,
and WireGuard-only administrative access. Do not expose the Kubernetes API or
Mergen Core publicly.

Build and publish the Core image to a private/approved registry, then replace
`ghcr.io/enessanc/mergen:dev` with its immutable digest in `core.yaml`.

```bash
kubectl apply -f infrastructure/kubernetes/core/namespace-rbac.yaml
kubectl apply -f infrastructure/kubernetes/core/core.yaml
kubectl -n mergen rollout status deployment/mergen-core
kubectl -n mergen port-forward service/mergen-core 8080:8080
```

Verify RBAC before running any agent workload:

```bash
kubectl auth can-i create jobs --as=system:serviceaccount:mergen:mergen-core -n mergen
kubectl auth can-i create jobs --as=system:serviceaccount:mergen:mergen-agent -n mergen
```

The first command must be `yes`; the second must be `no`. Never mount a Docker
socket, hostPath, kubeconfig, or broad Git/provider credential into an agent Pod.
