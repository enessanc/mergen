from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from .domain import Execution, ExecutionState


class SQLiteStore:
    def __init__(self, path: str = "mergen.db"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""CREATE TABLE IF NOT EXISTS executions (id TEXT PRIMARY KEY, project_id TEXT NOT NULL, work_item_id TEXT NOT NULL UNIQUE, state TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, execution_id TEXT NOT NULL, type TEXT NOT NULL, payload TEXT NOT NULL, created_at TEXT NOT NULL);""")

    def save(self, execution: Execution, event_type: str, payload: dict | None = None) -> None:
        self.db.execute("INSERT INTO executions VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET state=excluded.state, updated_at=excluded.updated_at", (execution.id, execution.project_id, execution.work_item_id, execution.state.value, execution.created_at.isoformat(), execution.updated_at.isoformat()))
        self.db.execute("INSERT INTO events(execution_id,type,payload,created_at) VALUES(?,?,?,?)", (execution.id, event_type, json.dumps(payload or {}), execution.updated_at.isoformat()))
        self.db.commit()

    def get(self, execution_id: str) -> Execution | None:
        row = self.db.execute("SELECT * FROM executions WHERE id=?", (execution_id,)).fetchone()
        return None if row is None else Execution(row["id"], row["project_id"], row["work_item_id"], ExecutionState(row["state"]), __import__("datetime").datetime.fromisoformat(row["created_at"]), __import__("datetime").datetime.fromisoformat(row["updated_at"]))

    def by_work_item(self, work_item_id: str) -> Execution | None:
        row = self.db.execute("SELECT id FROM executions WHERE work_item_id=?", (work_item_id,)).fetchone()
        return self.get(row["id"]) if row else None
