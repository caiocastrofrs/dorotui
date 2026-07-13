import json
from pathlib import Path
from typing import TypedDict

from platformdirs import user_data_dir

DATA_DIR = Path(user_data_dir("doro-tui"))
DATA_FILE = DATA_DIR / "tasks.json"


def load_sessions() -> list:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

class TaskType(TypedDict):
    id: str
    name: str
    completed_sessions: int
    total_sessions: int

def save_session(session: TaskType) -> bool:
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        sessions = load_sessions()
        sessions.append(session)
        with open(DATA_FILE, "w") as f:
            json.dump(sessions, f, indent=2)
        return True
    except Exception as e:
        print(e)
        return False

def erase_all_data() -> bool:
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, "w") as f:
                json.dump([],f)
        return True
    except Exception as e:
        print(e)
        return False
