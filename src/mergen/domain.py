from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4


class ExecutionState(str, Enum):
    CREATED = "created"
    VALIDATING = "validating"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    VALIDATING_RESULT = "validating_result"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"


TERMINAL = {ExecutionState.COMPLETED, ExecutionState.FAILED, ExecutionState.STOPPED}
TRANSITIONS = {
    ExecutionState.CREATED: {ExecutionState.VALIDATING, ExecutionState.STOPPED},
    ExecutionState.VALIDATING: {ExecutionState.SCHEDULED, ExecutionState.FAILED, ExecutionState.STOPPED},
    ExecutionState.SCHEDULED: {ExecutionState.RUNNING, ExecutionState.FAILED, ExecutionState.STOPPED},
    ExecutionState.RUNNING: {ExecutionState.VALIDATING_RESULT, ExecutionState.FAILED, ExecutionState.STOPPED},
    ExecutionState.VALIDATING_RESULT: {ExecutionState.COMPLETED, ExecutionState.FAILED},
    ExecutionState.COMPLETED: set(), ExecutionState.FAILED: set(), ExecutionState.STOPPED: set(),
}


class InvalidTransition(ValueError):
    pass


@dataclass(frozen=True)
class Execution:
    id: str
    project_id: str
    work_item_id: str
    state: ExecutionState
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(cls, project_id: str, work_item_id: str) -> "Execution":
        now = datetime.now(timezone.utc)
        return cls(str(uuid4()), project_id, work_item_id, ExecutionState.CREATED, now, now)

    def transition(self, target: ExecutionState) -> "Execution":
        if target not in TRANSITIONS[self.state]:
            raise InvalidTransition(f"{self.state.value} -> {target.value} is not allowed")
        return Execution(self.id, self.project_id, self.work_item_id, target, self.created_at, datetime.now(timezone.utc))
