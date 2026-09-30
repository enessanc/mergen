import pytest
from mergen.harness import HarnessError, run_validation
from mergen.git_lifecycle import GitLifecycleError, create_task_branch

def test_validation_rejects_failure(tmp_path):
    with pytest.raises(HarnessError): run_validation([["python3", "-c", "raise SystemExit(1)"]], str(tmp_path))

def test_protected_branch_is_rejected(tmp_path):
    with pytest.raises(GitLifecycleError): create_task_branch(str(tmp_path), "dev-agent", "main")
