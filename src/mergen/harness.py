from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Harness:
    name: str
    executable: str
    arguments: tuple[str, ...] = ()

BUILT_INS = {
    "codex": Harness("codex", "codex", ("exec",)),
    "claude-code": Harness("claude-code", "claude", ()),
    "aider": Harness("aider", "aider", ()),
}

class HarnessError(RuntimeError): pass

def run_harness(harness: Harness, instruction: str, workspace: str, environment: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    if not Path(workspace).is_dir(): raise HarnessError("workspace does not exist")
    env = {**os.environ, **(environment or {})}
    return subprocess.run([harness.executable, *harness.arguments, instruction], cwd=workspace, env=env, text=True, capture_output=True, check=False)

def run_validation(commands: list[list[str]], workspace: str) -> None:
    for command in commands:
        result = subprocess.run(command, cwd=workspace, text=True, capture_output=True, check=False)
        if result.returncode:
            raise HarnessError(f"validation failed: {command!r}\n{result.stdout}\n{result.stderr}")
