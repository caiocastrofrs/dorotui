from textual.app import App
from textual.reactive import reactive

from configuration import load_config, save_config
from screens.dashboard import DashboardScreen
from screens.settings import SettingsScreen
from screens.tasks import TasksScreen
from screens.timer import TimerScreen


class DorotuiApp(App):
    config = load_config()

    CSS_PATH="styles/styles.tcss"
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
        "tasks": TasksScreen
    }

    default_focus_time: reactive[int] = reactive(config['default_focus_time'])
    default_rest_time: reactive[int] = reactive(config['default_rest_time'])

    def on_mount(self) -> None:
        self.theme = self.config['theme']
        self.switch_mode('timer')

    def action_toggle_dark(self) -> None:
        self.theme = ("textual-dark" if self.theme == "textual-light" else "textual-light")

    def watch_theme(self) -> None:
        if not self.theme == self.config['theme']:
            self.config['theme'] = self.theme
            save_config(self.config)

if __name__ == "__main__":
    app = DorotuiApp()
    app.run()
