from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Footer, Header

from configuration import load_config, save_config
from widgets.doro_timer import DoroTimer
from widgets.timer_config import TimerConfig


class DorotuiApp(App):
    CSS_PATH="styles/doro.tcss"
    BINDINGS = [
            ("d", "toggle_dark", "Toggle Dark Mode"),
            ("p", "toggle_config", "Toggle Configuration"),
            ]

    is_config_open = reactive(False, recompose=True)
    config = load_config()

    default_time = reactive(3600.00 * config['default_session_time'], recompose=True ) #25 Minutes 
    default_rest = reactive(3600.00 * config['default_rest_time'], recompose=True) #5 Minutes
    
    def on_mount(self) -> None:
        self.theme = self.config['theme']

    def compose(self) -> ComposeResult:
        yield Header()

        if self.is_config_open:
            yield TimerConfig()
        else:
            yield DoroTimer()

        yield Footer()
    
    def action_toggle_config(self) -> None:
        self.is_config_open = (False if self.is_config_open else True)

    def action_toggle_dark(self) -> None:
        self.theme = ("textual-dark" if self.theme == "textual-light" else "textual-light")

    def watch_theme(self) -> None:
        if not self.theme == self.config['theme']:
            self.config['theme'] = self.theme
            save_config(self.config)

if __name__ == "__main__":
    app = DorotuiApp()
    app.run()
