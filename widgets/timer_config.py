from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import CenterMiddle, HorizontalGroup
from textual.widgets import Button, Input, Label

from configuration import load_config, save_config

if TYPE_CHECKING:
    from doro import DorotuiApp

class TimerConfig(CenterMiddle):
    app: "DorotuiApp"

    session_input  = Input(placeholder="25", type="integer", id="session")
    rest_input = Input(placeholder="5", type="integer", id="rest")

    def compose(self) -> ComposeResult:
        yield Label("Session time (in minutes)")
        yield self.session_input
        
        yield Label("Rest time (in minutes)")
        yield self.rest_input

        yield HorizontalGroup(Button('Save', id="save"), Button('Reset to Default', id="default"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        config = load_config()
        if event.button.id == "save":
            session_value = self.session_input.value
            rest_value = self.rest_input.value
            
            if session_value:
                self.app.default_time = int(session_value) * 3600
                config['default_session_time'] = int(session_value)
                self.notify(f'Session time set to {session_value}')
            if rest_value:
                self.app.default_rest = int(rest_value) * 3600
                config['default_rest_time'] = int(rest_value)
                self.notify(f'Rest time set to {rest_value}')

        if event.button.id == "default":
            config['default_session_time'] = 25
            config['default_rest_time'] = 5
            self.app.default_time = 25 * 3600
            self.app.default_rest = 5 * 3600
            self.notify('All settings restored to default.')

        save_config(config)
