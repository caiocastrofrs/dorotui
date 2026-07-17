from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Label

from widgets.header import CHeader


class DashboardScreen(Screen):
    def compose(self) -> ComposeResult:
        yield CHeader()
        yield Label("Dashboard")
        yield Footer()
