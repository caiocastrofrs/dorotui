
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Footer, Header

from widgets.doro_timer import DoroTimer
from widgets.timer_config import TimerConfig


class Dorotui(App):
    CSS_PATH="styles/doro.tcss"
    BINDINGS = [
            ("d", "toggle_dark", "Toggle Dark Mode"),
            ("p", "toggle_config", "Toggle Configuration"),
            ]

    is_config_open = reactive(False, recompose=True)
    default_time = reactive(3600.00 * 25.00, recompose=True) # 25 Minutes 
    default_rest = reactive(3600.00 * 5.00, recompose=True) # 5 Minutes
    
    def compose(self) -> ComposeResult:
        self.theme = "flexoki"
        yield Header()

        if self.is_config_open:
            yield TimerConfig()
        else:
            yield DoroTimer()

        yield Footer()
    
    def action_toggle_config(self) -> None:
        self.is_config_open = (False if self.is_config_open else True)

    def action_toggle_dark(self) -> None:
        self.theme = ("flexoki" if self.theme == "catppuccin-latte" else "catppuccin-latte")


if __name__ == "__main__":
    app = Dorotui()
    app.run()
