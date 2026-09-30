from __future__ import annotations

import subprocess

class GitLifecycleError(RuntimeError): pass

def git(workspace: str, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=workspace, text=True, capture_output=True, check=False)
    if result.returncode: raise GitLifecycleError(result.stderr.strip())
    return result.stdout.strip()

def create_task_branch(workspace: str, base_branch: str, branch: str) -> None:
    if branch in {"main", "dev-user", "dev-agent"} or not branch.startswith("agent/"):
        raise GitLifecycleError("task branch must use agent/ prefix and may not target protected branches")
    git(workspace, "fetch", "origin", base_branch)
    git(workspace, "switch", "--create", branch, f"origin/{base_branch}")

def commit_and_push_task(workspace: str, message: str) -> tuple[str, str]:
    git(workspace, "add", "--all")
    git(workspace, "commit", "--message", message)
    branch = git(workspace, "branch", "--show-current")
    if not branch.startswith("agent/"): raise GitLifecycleError("refusing to push a non-task branch")
    git(workspace, "push", "--set-upstream", "origin", branch)
    return branch, git(workspace, "rev-parse", "HEAD")
