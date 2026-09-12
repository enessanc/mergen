from __future__ import annotations

import subprocess
from typing import Protocol


class Runner(Protocol):
    def create(self, manifest: str) -> str: ...
    def stop(self, namespace: str, job_name: str) -> None: ...


class KubernetesRunner:
    """Trusted control-plane adapter; Pods never receive kubectl credentials."""
    def __init__(self, kubectl: str = "kubectl"):
        self.kubectl = kubectl

    def create(self, manifest: str) -> str:
        result = subprocess.run([self.kubectl, "apply", "--filename", "-"], input=manifest, text=True, capture_output=True, check=True)
        return result.stdout

    def stop(self, namespace: str, job_name: str) -> None:
        subprocess.run([self.kubectl, "--namespace", namespace, "delete", "job", job_name, "--ignore-not-found=true"], text=True, capture_output=True, check=True)
