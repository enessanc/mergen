from .domain import Execution, ExecutionState, InvalidTransition, TERMINAL
from .runner import JobState, Runner
from .store import SQLiteStore


class Controller:
    def __init__(self, store: SQLiteStore, runner: Runner): self.store, self.runner = store, runner

    def create(self, project_id: str, work_item_id: str, manifest: str, namespace: str, job_name: str) -> Execution:
        if self.store.by_work_item(work_item_id): raise ValueError("work item already has an execution")
        execution = Execution.create(project_id, work_item_id)
        self.store.save(execution, "TASK_ACCEPTED", {"job_name": job_name})
        execution = execution.transition(ExecutionState.VALIDATING); self.store.save(execution, "VALIDATING")
        execution = execution.transition(ExecutionState.SCHEDULED); self.store.save(execution, "SCHEDULED", {"namespace": namespace, "job_name": job_name})
        try: self.runner.create(manifest)
        except Exception as error:
            execution = execution.transition(ExecutionState.FAILED); self.store.save(execution, "FAILED", {"reason": str(error)})
        return execution

    def reconcile(self, execution_id: str, namespace: str, job_name: str) -> Execution:
        execution = self.store.get(execution_id)
        if execution is None or execution.state in TERMINAL: return execution
        state = self.runner.observe(namespace, job_name)
        target = {JobState.PENDING: ExecutionState.SCHEDULED, JobState.RUNNING: ExecutionState.RUNNING, JobState.SUCCEEDED: ExecutionState.VALIDATING_RESULT, JobState.FAILED: ExecutionState.FAILED, JobState.MISSING: ExecutionState.FAILED}[state]
        if target != execution.state:
            execution = execution.transition(target); self.store.save(execution, target.value.upper())
        return execution

    def stop(self, execution_id: str, namespace: str, job_name: str) -> Execution:
        execution = self.store.get(execution_id)
        if execution is None: return None
        self.runner.stop(namespace, job_name)
        if execution.state not in TERMINAL:
            execution = execution.transition(ExecutionState.STOPPED); self.store.save(execution, "STOPPED")
        return execution
