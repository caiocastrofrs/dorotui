from textual.app import App
from textual.reactive import reactive

from configuration import DefaultConfigType, load_config, save_config
from data import TaskType, load_sessions, save_sessions
from screens.dashboard import DashboardScreen
from screens.settings import SettingsScreen
from screens.tasks import TasksScreen
from screens.timer import TimerScreen


class DorotuiApp(App):
    CSS_PATH = "styles/styles.tcss"
    BINDINGS = [
        ("p", "toggle_dark", "Toggle Dark Mode"),
        ("d", "switch_mode('dashboard')", "Dashboard"),
        ("t", "switch_mode('timer')", "Timer"),
        ("r", "switch_mode('tasks')", "Tasks"),
        ("s", "switch_mode('settings')", "Settings"),
    ]

    MODES = {
        "dashboard": DashboardScreen,
        "settings": SettingsScreen,
        "timer": TimerScreen,
        "tasks": TasksScreen,
    }

    config: reactive[DefaultConfigType] = reactive(load_config())
    saved_data: reactive[list[TaskType]] = reactive(load_sessions())

    def on_mount(self) -> None:
        self.theme = self.config["theme"]
        self.switch_mode("timer")

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def get_current_task(self) -> TaskType | None:
        for task in self.saved_data:
            if task["id"] == self.config["current_task_id"]:
                return task
        return None

    def remove_one_task(self, task_id_to_remove) -> TaskType | None:
        updated_data = self.saved_data.copy()
        for task in self.saved_data:
            if task["id"] == task_id_to_remove:
                updated_data.remove(task)
                self.saved_data = updated_data
                break

    def watch_config(self, new_config: DefaultConfigType):
        save_config(new_config)

    def watch_saved_data(self, new_data: list[TaskType]):
        save_sessions(new_data)

    def watch_theme(self) -> None:
        if not self.theme == self.config["theme"]:
            self.config["theme"] = self.theme
            save_config(self.config)


def main() -> None:
    app = DorotuiApp()
    app.run()


if __name__ == "__main__":
    main()
