
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from widgets.doro_timer import DoroTimer


class Dorotui(App):
    CSS_PATH="doro.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle Dark Mode")]

    def compose(self) -> ComposeResult:
        self.theme = "flexoki"
        yield Header()
        yield DoroTimer()
        yield Footer()

    
    def action_toggle_dark(self) -> None:
        self.theme = (
                "flexoki" if self.theme == "catppuccin-latte" else "catppuccin-latte"
                )


if __name__ == "__main__":
    app = Dorotui()
    app.run()
