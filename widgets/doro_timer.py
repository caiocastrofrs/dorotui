import subprocess

from textual.app import ComposeResult
from textual.containers import CenterMiddle
from textual.reactive import reactive
from textual.widgets import Button, Digits


class TimeDisplay(Digits):
    default_time = 3600.00 * 25.00 # 25 minutes 

    time = reactive(200)  # noqa: F821

    def on_mount(self) -> None:
        self.update_timer = self.set_interval(1/60, self.update_time, pause=True)

    def update_time(self) -> None:
        if self.time > 0:
            self.time -= 1
        else:
            self.stop()
            self.reset()
            self.query_ancestor(DoroTimer).remove_class("started")
            subprocess.run(["paplay","--volume=30000","sounds/alarm-clock-elapsed.oga"])


    def watch_time(self, time: float) -> None:
        seconds, _ = divmod(time, 60)
        minutes, seconds = divmod(seconds, 60)

        self.update(f"{minutes:02,.0f}:{seconds:02.0f}")

    def start(self) -> None:
        self.update_timer.resume()

    def stop(self) -> None:
        self.update_timer.pause()

    def reset(self) -> None:
        self.time = self.default_time

class DoroTimer(CenterMiddle):
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

    def compose(self) -> ComposeResult:
        time_display = TimeDisplay()
        start = Button("Start", id="start")
        stop = Button("Stop", id="stop")
        reset = Button("Reset", id="reset")
        yield time_display
        yield start
        yield stop
        yield reset
