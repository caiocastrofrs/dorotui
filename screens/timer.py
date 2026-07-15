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

    default_time: reactive[int] = reactive(0)
    current_timer = 'focus'

    def on_mount(self) -> None:
        self.time = self.config['default_focus_time'] * 3600
        if self.current_timer == 'focus':
            self.update_default_time(self.app.config['default_focus_time'])
        elif self.current_timer == 'rest':
            self.update_default_time(self.app.config['default_rest_time'])
        self.update_timer = self.set_interval(1/60, self.update_time, pause=True)

    def update_default_time(self, new_time) -> None:
        self.default_time = new_time


    def update_time(self) -> None:
        if self.time > 0:
            self.time -= 1
        else:
            self.stop()
            self.reset()
            subprocess.run(["paplay","--volume=30000","sounds/alarm-clock-elapsed.oga"])
            self.query_ancestor(TimerScreen).remove_class("started")
            self.toggle_timer()

    def watch_default_time(self) -> None:
        self.time = self.default_time * 3600

    def watch_time(self, time: int) -> None:
        seconds, _ = divmod(time, 60)
        minutes, seconds = divmod(seconds, 60)
        self.update(f"{minutes:02,.0f}:{seconds:02.0f}")

    def start(self) -> None:
        self.update_timer.resume()

    def stop(self) -> None:
        self.update_timer.pause()

    def reset(self) -> None:
        if self.current_timer == 'focus':
            self.time = self.app.config['default_focus_time'] * 3600
        elif self.current_timer == 'rest':
            self.time = self.app.config['default_rest_time'] * 3600

    def toggle_timer(self) -> None:
        if self.current_timer == 'focus':
            self.current_timer = 'rest'
            self.time = self.app.config['default_rest_time'] * 3600
        elif self.current_timer == 'rest':
            self.current_timer = 'focus'
            self.time = self.app.config['default_focus_time'] * 3600

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
        elif button_id == "stop":
            time_display.stop()
            self.remove_class("started")
        elif button_id == "reset":
            time_display.reset()

    def on_screen_resume(self) -> None:
        if self.time_display.current_timer == 'focus':
            self.time_display.update_default_time(self.app.config['default_focus_time'])
        elif self.time_display.current_timer == 'rest':
            self.time_display.update_default_time(self.app.config['default_rest_time'])

    def compose(self) -> ComposeResult:
        yield CHeader()
        with CenterMiddle():
            yield self.time_display
            yield Button("Start", id="start")
            yield Button("Stop", id="stop")
            yield Button("Reset", id="reset")
        yield Footer()
