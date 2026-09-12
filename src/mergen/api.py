from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .controller import Controller
from .runner import KubernetesRunner, Runner
from .store import SQLiteStore

class CreateExecution(BaseModel):
    project_id: str = Field(min_length=1)
    work_item_id: str = Field(min_length=1)
    manifest: str = Field(min_length=1)
    namespace: str = Field(min_length=1)
    job_name: str = Field(min_length=1)

def serialize(e):
    return {"id": e.id, "project_id": e.project_id, "work_item_id": e.work_item_id, "state": e.state, "created_at": e.created_at, "updated_at": e.updated_at}

def create_app(store: SQLiteStore | None = None, runner: Runner | None = None) -> FastAPI:
    store, runner = store or SQLiteStore(), runner or KubernetesRunner()
    controller = Controller(store, runner)
    app = FastAPI(title="Mergen Core", version="0.1.0")
    @app.post("/executions", status_code=201)
    def create_execution(request: CreateExecution):
        try: return serialize(controller.create(**request.model_dump()))
        except ValueError as error: raise HTTPException(409, str(error))
    @app.get("/executions/{execution_id}")
    def get_execution(execution_id: str):
        execution = store.get(execution_id)
        if not execution: raise HTTPException(404, "execution not found")
        return serialize(execution)
    @app.post("/executions/{execution_id}/reconcile")
    def reconcile(execution_id: str, namespace: str, job_name: str):
        execution = controller.reconcile(execution_id, namespace, job_name)
        if not execution: raise HTTPException(404, "execution not found")
        return serialize(execution)
    @app.post("/executions/{execution_id}/stop")
    def stop(execution_id: str, namespace: str, job_name: str):
        execution = controller.stop(execution_id, namespace, job_name)
        if not execution: raise HTTPException(404, "execution not found")
        return serialize(execution)
    return app

app = create_app()
