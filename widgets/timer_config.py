from textual.app import ComposeResult
from textual.containers import CenterMiddle, HorizontalGroup
from textual.widgets import Button, Input, Label


class TimerConfig(CenterMiddle):
    session_input  = Input(placeholder="25", type="integer", id="session")
    rest_input = Input(placeholder="5", type="integer", id="rest")

    def compose(self) -> ComposeResult:
        # Session time
        yield Label("Session time (in minutes)")
        yield self.session_input
        yield Label("Rest time (in minutes)")
        yield self.rest_input
        yield HorizontalGroup(Button('Save', id="save"), Button('Reset to Default', id="default"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            session_value = self.session_input.value
            rest_value = self.rest_input.value
            
            if session_value and rest_value:
                self.app.default_time = int(session_value) * 3600
                self.app.default_rest =  int(rest_value) * 3600
        if event.button.id == "default":
            self.app.default_time = 3600 * 25
            self.app.default_rest = 3600 * 5
