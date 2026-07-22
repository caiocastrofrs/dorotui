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


def save_sessions(sessions_list: list[TaskType]) -> None:
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(sessions_list, f, indent=2)
    except Exception as e:
        print(e)
