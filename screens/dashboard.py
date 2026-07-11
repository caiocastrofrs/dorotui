from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Label


class DashboardScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label('Dashboard')
        yield Footer()
