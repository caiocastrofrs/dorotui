from pathlib import Path
from typing import TypedDict, cast

import tomli_w
import tomllib
from platformdirs import user_config_dir

CONFIG_DIR = Path(user_config_dir("doro-tui"))
CONFIG_FILE = CONFIG_DIR / "config.toml"


class DefaultConfigType(TypedDict):
    default_focus_time: int
    default_rest_time: int
    theme: str
    current_task_id: str


DEFAULT_CONFIG: DefaultConfigType = {
    "default_focus_time": 25,
    "default_rest_time": 5,
    "theme": "textual-dark",
    "current_task_id": "",
}


def load_config() -> DefaultConfigType:
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with open(CONFIG_FILE, "rb") as f:
        return cast(DefaultConfigType, tomllib.load(f))


def save_config(config: DefaultConfigType) -> DefaultConfigType:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "wb") as f:
        tomli_w.dump(config, f)
    return config
