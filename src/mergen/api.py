from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .domain import Execution, ExecutionState, InvalidTransition
from .store import SQLiteStore

store = SQLiteStore()
app = FastAPI(title="Mergen Core", version="0.1.0")

class CreateExecution(BaseModel):
    project_id: str = Field(min_length=1)
    work_item_id: str = Field(min_length=1)

def serialize(e: Execution) -> dict:
    return {"id": e.id, "project_id": e.project_id, "work_item_id": e.work_item_id, "state": e.state, "created_at": e.created_at, "updated_at": e.updated_at}

@app.post("/executions", status_code=201)
def create_execution(request: CreateExecution):
    existing = store.db.execute("SELECT id FROM executions WHERE work_item_id=?", (request.work_item_id,)).fetchone()
    if existing:
        raise HTTPException(409, "work item already has an execution")
    execution = Execution.create(request.project_id, request.work_item_id)
    store.save(execution, "TASK_ACCEPTED")
    execution = execution.transition(ExecutionState.VALIDATING)
    store.save(execution, "VALIDATING")
    return serialize(execution)

@app.get("/executions/{execution_id}")
def get_execution(execution_id: str):
    execution = store.get(execution_id)
    if execution is None: raise HTTPException(404, "execution not found")
    return serialize(execution)

@app.post("/executions/{execution_id}/stop")
def stop_execution(execution_id: str):
    execution = store.get(execution_id)
    if execution is None: raise HTTPException(404, "execution not found")
    try: execution = execution.transition(ExecutionState.STOPPED)
    except InvalidTransition as error: raise HTTPException(409, str(error))
    store.save(execution, "STOPPED")
    return serialize(execution)
