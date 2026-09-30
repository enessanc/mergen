from __future__ import annotations
import json
import subprocess
from enum import Enum
from typing import Protocol

class JobState(str, Enum):
    PENDING = "pending"; RUNNING = "running"; SUCCEEDED = "succeeded"; FAILED = "failed"; MISSING = "missing"

class Runner(Protocol):
    def create(self, manifest: str) -> str: ...
    def observe(self, namespace: str, job_name: str) -> JobState: ...
    def stop(self, namespace: str, job_name: str) -> None: ...

class KubernetesRunner:
    """Trusted control-plane adapter; Pods never receive kubectl credentials."""
    def __init__(self, kubectl: str = "kubectl"): self.kubectl = kubectl
    def create(self, manifest: str) -> str:
        return subprocess.run([self.kubectl, "apply", "--filename", "-"], input=manifest, text=True, capture_output=True, check=True).stdout
    def observe(self, namespace: str, job_name: str) -> JobState:
        result = subprocess.run([self.kubectl, "--namespace", namespace, "get", "job", job_name, "--output=json"], text=True, capture_output=True)
        if result.returncode: return JobState.MISSING
        status = json.loads(result.stdout).get("status", {})
        if status.get("succeeded"): return JobState.SUCCEEDED
        if status.get("failed"): return JobState.FAILED
        return JobState.RUNNING if status.get("active") else JobState.PENDING
    def stop(self, namespace: str, job_name: str) -> None:
        subprocess.run([self.kubectl, "--namespace", namespace, "delete", "job", job_name, "--ignore-not-found=true"], text=True, capture_output=True, check=True)
