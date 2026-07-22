import uuid
from typing import TYPE_CHECKING, cast

from textual.app import ComposeResult
from textual.containers import Center, CenterMiddle, HorizontalGroup, VerticalGroup
from textual.reactive import reactive
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, Footer, Input, Label, ListItem, ListView

from data import (
    TaskType,
)
from widgets.header import CHeader

if TYPE_CHECKING:
    from app import DorotuiApp


class CreateTaskModal(ModalScreen[TaskType]):
    def compose(self) -> ComposeResult:
        with CenterMiddle():
            yield VerticalGroup(
                Label("Task name:"),
                Input(placeholder="Daily study", type="text", id="input_task_name"),
                Label("Total sessions:"),
                Input(placeholder="10", type="integer", id="input_total_sessions"),
                HorizontalGroup(
                    Button("Create", variant="default", id="button_create_task"),
                    Button("Cancel", variant="primary", id="button_cancel"),
                    id="button_box",
                ),
                id="dialog_create_task",
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "button_create_task":
            task_name = self.query_exactly_one("#input_task_name", Input).value
            total_sessions = int(
                self.query_exactly_one("#input_total_sessions", Input).value
            )
            new_id = uuid.uuid4()

            if task_name and total_sessions:
                task: TaskType = {
                    "id": str(new_id)[0:8],
                    "name": task_name,
                    "completed_sessions": 0,
                    "total_sessions": int(total_sessions),
                }

                self.dismiss(task)
            elif not total_sessions:
                self.notify("1 is the minimum allowed value", severity="warning")
            else:
                self.notify("Fill the required inputs", severity="warning")
        else:
            self.app.pop_screen()


class Task(ListItem):
    app: "DorotuiApp"

    completed_sessions: reactive[int] = reactive(0, recompose=True)

    def __init__(
        self, task_id: str, task_name: str, total_sessions: int, completed_sessions: int
    ):
        super().__init__()
        self.task_id = task_id
        self.task_name = task_name
        self.total_sessions = total_sessions
        self.completed_sessions = completed_sessions

    def on_mount(self) -> None:
        if self.app.config["current_task_id"] == self.task_id:
            self.add_class("current_task")

    def watch_completed_sessions(self) -> None:
        updated_data = self.app.saved_data.copy()
        for index, task in enumerate(updated_data):
            if task["id"] == self.task_id:
                updated_data[index]["completed_sessions"] = self.completed_sessions
        self.app.saved_data = updated_data

    def compose(self) -> ComposeResult:
        yield Label(str(self.task_id))
        yield Label(self.task_name, id="task_name_label")
        yield Label(
            f"󱎫 {self.completed_sessions} completed of 󱎫 {self.total_sessions}",
            classes="task_sessions",
        )


class TaskList(ListView):
    app: "DorotuiApp"

    BINDINGS = [
        ("ctrl+d", "erase_all_tasks", "Erase all tasks"),
        ("D", "delete_one_task", "Delete selected task"),
        ("ctrl+t", "create_task", "Create Task"),
        ("+", "increase_completed_session", "Inc completed sessions by 1"),
        ("-", "decrease_completed_session", "Dec completed sessions by 1"),
    ]

    async def on_mount(self) -> None:
        await self.populate_tasks()

    async def populate_tasks(self) -> None:
        await self.clear()
        list_items = []
        for data in self.app.saved_data:
            list_items.append(
                Task(
                    data["id"],
                    data["name"],
                    data["total_sessions"],
                    data["completed_sessions"],
                )
            )
        await self.extend(list_items)

    def on_list_view_selected(self, selected: ListView.Selected) -> None:
        selected_item_task_id = cast(Task, selected.item).task_id
        if not selected_item_task_id == self.app.config["current_task_id"]:
            updated_config = self.app.config.copy()
            updated_config["current_task_id"] = selected_item_task_id
            self.app.config = updated_config
            self.toggle_current_task_class(selected)
        else:
            self.notify(
                f"{selected_item_task_id} task already set to main",
                severity="information",
            )

    def toggle_current_task_class(self, selected: ListView.Selected) -> None:
        for item in self.children:
            if not item.id != selected.item.id:
                item.remove_class("current_task")
        selected.item.add_class("current_task")

    def action_increase_completed_session(self) -> None:
        selected_task = cast(Task, self.highlighted_child)
        if not selected_task:
            self.notify("No task selected")
            return
        if selected_task.completed_sessions == selected_task.total_sessions:
            self.notify("Max completed sessions reached!")
        else:
            selected_task.completed_sessions += 1

    def action_decrease_completed_session(self) -> None:
        selected_task = cast(Task, self.highlighted_child)
        if not selected_task:
            self.notify("No task selected")
            return
        if selected_task.completed_sessions == 0:
            self.notify("Can't decrease below 0!")
        else:
            selected_task.completed_sessions -= 1

    def action_erase_all_tasks(self) -> None:
        self.clear()
        self.app.saved_data = []
        self.app.config["current_task_id"] = ""

    def action_delete_one_task(self) -> None:
        selected_task = cast(Task, self.highlighted_child)
        if selected_task:
            for index, list_item in enumerate(self.children):
                if list_item == selected_task:
                    self.pop(index)

            self.app.remove_one_task(selected_task.task_id)
            self.notify(f"task {selected_task.task_id} was deleted")

    def action_create_task(self):
        def handle_new_task(new_task: TaskType | None) -> None:
            if new_task:
                self.app.saved_data.append({**new_task, "completed_sessions": 0})

        self.app.push_screen(CreateTaskModal(), handle_new_task)


class TasksScreen(Screen):
    CSS_PATH = "../styles/tasks.tcss"

    def on_mount(self) -> None:
        self.title = " Tasks"

    async def on_screen_resume(self) -> None:
        await self.query_one(TaskList).populate_tasks()

    def compose(self) -> ComposeResult:
        yield CHeader()
        with Center():
            yield TaskList()
        yield Footer()
