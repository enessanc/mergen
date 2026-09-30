from mergen.controller import Controller
from mergen.domain import ExecutionState
from mergen.runner import JobState
from mergen.store import SQLiteStore

class FakeRunner:
    def __init__(self, state=JobState.RUNNING): self.state, self.created, self.stopped = state, [], []
    def create(self, manifest): self.created.append(manifest); return "created"
    def observe(self, namespace, job_name): return self.state
    def stop(self, namespace, job_name): self.stopped.append((namespace, job_name))

def test_controller_dispatches_reconciles_and_stops(tmp_path):
    runner = FakeRunner(); controller = Controller(SQLiteStore(str(tmp_path / "db.sqlite")), runner)
    execution = controller.create("p", "w", "apiVersion: batch/v1", "ns", "job")
    assert execution.state is ExecutionState.SCHEDULED
    assert controller.reconcile(execution.id, "ns", "job").state is ExecutionState.RUNNING
    assert controller.stop(execution.id, "ns", "job").state is ExecutionState.STOPPED
