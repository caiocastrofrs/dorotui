from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import CenterMiddle, HorizontalGroup
from textual.screen import Screen
from textual.widgets import Button, Footer, Input, Label

from configuration import DEFAULT_CONFIG
from widgets.header import CHeader

if TYPE_CHECKING:
    from app import DorotuiApp


class SettingsScreen(Screen):
    CSS_PATH = "../styles/settings.tcss"
    app: "DorotuiApp"

    def on_mount(self) -> None:
        self.title = " Settings"

    def compose(self) -> ComposeResult:
        yield CHeader()
        with CenterMiddle():
            yield Label("Focus time (in minutes)")
            yield Input(placeholder="25", type="integer", id="focus_time")
            yield Label("Rest time (in minutes)")
            yield Input(placeholder="5", type="integer", id="rest_time")
            with HorizontalGroup():
                yield Button("Save", id="save")
                yield Button("Reset to Default", id="default")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        updated_config = self.app.config.copy()
        if event.button.id == "save":
            focus_time = self.query_exactly_one("#focus_time", Input).value
            rest_time = self.query_exactly_one("#rest_time", Input).value

            if focus_time:
                if int(focus_time) < 1:
                    self.notify("1 is the minimum allowed value", severity="warning")
                    return

                updated_config["default_focus_time"] = int(focus_time)
                self.notify(f"Session time set to {focus_time}")

            if rest_time:
                if int(rest_time) < 1:
                    self.notify("1 is the minimum allowed value", severity="warning")
                    return

                updated_config["default_rest_time"] = int(rest_time)
                self.notify(f"Rest time set to {rest_time}")

            if not focus_time and not rest_time:
                self.notify("Fill atleast one input", severity="warning")
                return

        if event.button.id == "default":
            updated_config["default_focus_time"] = DEFAULT_CONFIG["default_focus_time"]
            updated_config["default_rest_time"] = DEFAULT_CONFIG["default_rest_time"]
            self.notify("All settings restored to default.")

        self.app.config = updated_config
