import json
from pathlib import Path
from typing import TypedDict

from platformdirs import user_data_dir

DATA_DIR = Path(user_data_dir("doro-tui"))
DATA_FILE = DATA_DIR / "tasks.json"


class TaskType(TypedDict):
    id: str
    name: str
    completed_sessions: int
    total_sessions: int

def load_sessions() -> list[TaskType]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_session(session: TaskType) -> list[TaskType] | None:
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        sessions = load_sessions()
        sessions.append(session)
        with open(DATA_FILE, "w") as f:
            json.dump(sessions, f, indent=2)
        return sessions
    except Exception as e:
        print(e)
