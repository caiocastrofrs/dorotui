import tomllib
from pathlib import Path

import tomli_w
from platformdirs import user_config_dir

CONFIG_DIR = Path(user_config_dir("doro-tui"))
CONFIG_FILE = CONFIG_DIR / "config.toml"

DEFAULT_CONFIG = {
    "default_focus_time": 25,
    "default_rest_time": 5,
    "theme": "textual-dark",
}


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with open(CONFIG_FILE, "rb") as f:
        return tomllib.load(f)


def save_config(config: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "wb") as f:
        tomli_w.dump(config, f)
