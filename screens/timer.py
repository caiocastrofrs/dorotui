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
            if self.current_timer == "focus":
                updated_data = self.app.saved_data.copy()
                current_task = self.app.get_current_task()
                if current_task:
                    index = updated_data.index(current_task)
                    updated_data[index] = {
                        **updated_data[index],
                        "completed_sessions": updated_data[index]["completed_sessions"]
                        + 1,
                    }
                    self.app.saved_data = updated_data
                    self.screen.query_one(CurrentTask).update_content()

            self.toggle_timer()
            self.query_ancestor(TimerScreen).remove_class("started")

    def watch_time(self, time: int) -> None:
        seconds, _ = divmod(time, 60)
        minutes, seconds = divmod(seconds, 60)
        self.update(f"{minutes:02,.0f}:{seconds:02.0f}")

    def start(self) -> bool:
        task = self.app.get_current_task()
        if task:
            if (
                task["completed_sessions"] == task["total_sessions"]
                and self.current_timer != "rest"
            ):
                self.notify("Current task already reached maximum sessions.")
            else:
                self.update_timer.resume()
                return True
        return False

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
    app: "DorotuiApp"

    def on_mount(self) -> None:
        self.update_content()

    def update_content(self) -> None:
        current_task = self.app.get_current_task()
        if current_task:
            self.update(
                f"{current_task['id']}\n{current_task['name']}\n{current_task['completed_sessions']}/{current_task['total_sessions']}"
            )
        else:
            self.update("No task selected")


class TimerScreen(Screen):
    CSS_PATH = "../styles/timer.tcss"
    app: "DorotuiApp"

    def on_mount(self) -> None:
        self.title = "󱎫 Timer"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "start":
            if self.query_one(TimeDisplay).start():
                self.add_class("started")
        elif button_id == "stop":
            self.query_one(TimeDisplay).stop()
            self.remove_class("started")
        elif button_id == "reset":
            self.query_one(TimeDisplay).reset()

    def on_screen_resume(self) -> None:
        self.query_one(TimeDisplay).reset()
        self.query_one(CurrentTask).update_content()

    def compose(self) -> ComposeResult:
        yield CHeader()
        with CenterMiddle():
            yield CurrentTask()
            yield TimeDisplay()
            with HorizontalGroup():
                yield Button("Start", id="start")
                yield Button("Stop", id="stop")
                yield Button("Reset", id="reset")
        yield Footer()
