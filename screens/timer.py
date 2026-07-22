import subprocess
from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import CenterMiddle, HorizontalGroup
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Digits, Footer, Label

from widgets.header import CHeader

if TYPE_CHECKING:
    from app import DorotuiApp


class TimeDisplay(Digits):
    app: "DorotuiApp"

    time = reactive(0)
    current_timer = "focus"

    def on_mount(self) -> None:
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self) -> None:
        if self.time > 0:
            self.time -= 500
        else:
            self.stop()
            subprocess.run(
                ["paplay", "--volume=30000", "sounds/alarm-clock-elapsed.oga"]
            )
            self.toggle_timer()
            self.query_ancestor(TimerScreen).remove_class("started")

    def watch_time(self, time: int) -> None:
        seconds, _ = divmod(time, 60)
        minutes, seconds = divmod(seconds, 60)
        self.update(f"{minutes:02,.0f}:{seconds:02.0f}")

    def start(self) -> None:
        self.update_timer.resume()

    def stop(self) -> None:
        self.update_timer.pause()

    def reset(self) -> None:
        self.time = (
            self.app.config["default_focus_time"]
            if self.current_timer == "focus"
            else self.app.config["default_rest_time"]
        ) * 3600

    def toggle_timer(self) -> None:
        self.current_timer = "focus" if self.current_timer == "rest" else "rest"
        self.toggle_class("rest")
        self.reset()


class CurrentTask(Label):
    pass


class TimerScreen(Screen):
    CSS_PATH = "../styles/timer.tcss"
    app: "DorotuiApp"
    time_display = TimeDisplay()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "start":
            self.time_display.start()
            self.add_class("started")
        elif button_id == "stop":
            self.time_display.stop()
            self.remove_class("started")
        elif button_id == "reset":
            self.time_display.reset()

    def on_screen_resume(self) -> None:
        self.time_display.reset()
        task_name = self.app.config["current_task"]["name"]
        task_id = self.app.config["current_task"]["id"]
        self.query_exactly_one(CurrentTask).update(f"{task_id}\n{task_name}")

    def compose(self) -> ComposeResult:
        yield CHeader()
        with CenterMiddle():
            yield CurrentTask()
            yield self.time_display
            with HorizontalGroup():
                yield Button("Start", id="start")
                yield Button("Stop", id="stop")
                yield Button("Reset", id="reset")
        yield Footer()
    def on_mount(self) -> None:
        self.title = "󱎫 Timer"

    def on_mount(self) -> None:
        self.title = "󱎫 Timer"

