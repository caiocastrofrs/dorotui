import subprocess
from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import CenterMiddle
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Digits, Footer

from configuration import load_config
from widgets.header import CHeader

if TYPE_CHECKING:
    from app import DorotuiApp

class TimeDisplay(Digits):
    app: "DorotuiApp"
    config = load_config()

    time = reactive(0)
    current_timer = 'focus'

    def on_mount(self) -> None:
        self.reset()
        self.update_timer = self.set_interval(1/60, self.update_time, pause=True)


    def update_time(self) -> None:
        if self.time > 0:
            self.time -= 500
        else:
            self.stop()
            self.reset()
            subprocess.run(["paplay","--volume=30000","sounds/alarm-clock-elapsed.oga"])
            self.query_ancestor(TimerScreen).remove_class("started")
            self.toggle_timer()

    def watch_time(self, time: int) -> None:
        seconds, _ = divmod(time, 60)
        minutes, seconds = divmod(seconds, 60)
        self.update(f"{minutes:02,.0f}:{seconds:02.0f}")

    def start(self) -> None:
        self.update_timer.resume()

    def stop(self) -> None:
        self.update_timer.pause()

    def reset(self) -> None:
        self.time = (self.app.config['default_focus_time'] if self.current_timer == 'focus' else self.app.config['default_rest_time']) * 3600

    def toggle_timer(self) -> None:
        self.current_timer = ('focus' if self.current_timer == 'rest' else 'rest')
        self.reset()

class TimerScreen(Screen):
    CSS_PATH="../styles/timer.tcss"
    app: "DorotuiApp"
    config = load_config()
    time_display = TimeDisplay()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        time_display = self.query_one(TimeDisplay)

        if button_id == "start":
            time_display.start()
            self.add_class("started")
            self.app.add_class('focus')
        elif button_id == "stop":
            time_display.stop()
            self.remove_class("started")
        elif button_id == "reset":
            time_display.reset()

    def on_screen_resume(self) -> None:
        self.time_display.reset()

    def compose(self) -> ComposeResult:
        yield CHeader()
        with CenterMiddle():
            yield self.time_display
            yield Button("Start", id="start")
            yield Button("Stop", id="stop")
            yield Button("Reset", id="reset")
        yield Footer()
