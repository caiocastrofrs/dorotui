from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import CenterMiddle, HorizontalGroup
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label

from configuration import load_config, save_config

if TYPE_CHECKING:
    from app import DorotuiApp

class SettingsScreen(Screen):
    app: "DorotuiApp"

    def compose(self) -> ComposeResult:
        yield Header()
        with CenterMiddle():
            yield Label("Focus time (in minutes)")
            yield Input(placeholder="25", type="integer", id="focus_time")
            yield Label("Rest time (in minutes)")
            yield Input(placeholder="5", type="integer", id="rest_time")
            with HorizontalGroup():
                yield Button('Save', id="save")
                yield Button('Reset to Default', id="default")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        config = load_config()

        if event.button.id == "save":
            focus_time = self.query_exactly_one("#focus_time", Input).value
            rest_time = self.query_exactly_one("#rest_time", Input).value
            
            if focus_time:
                config['default_focus_time'] = int(focus_time)
                self.app.default_focus_time = int(focus_time)
                self.notify(f'Session time set to {focus_time}')
            if rest_time:
                config['default_rest_time'] = int(rest_time)
                self.app.default_rest_time = int(rest_time)
                self.notify(f'Rest time set to {rest_time}')

        if event.button.id == "default":
            config['default_focus_time'] = 25
            config['default_rest_time'] = 5
            self.app.default_focus_time = 25
            self.app.default_rest_time = 5
            self.notify('All settings restored to default.')

        save_config(config)

        
