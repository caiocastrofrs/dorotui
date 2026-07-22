import uuid
from typing import TYPE_CHECKING, cast

from textual.app import ComposeResult
from textual.containers import Center, CenterMiddle, HorizontalGroup, VerticalGroup
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, Footer, Input, Label, ListItem, ListView

from configuration import save_config
from data import TaskType, delete_one_task, erase_all_data, load_sessions, save_session
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
    def __init__(self, task_id: str, task_name: str, total_sessions: int):
        super().__init__()
        self.task_id = task_id
        self.task_name = task_name
        self.total_sessions = total_sessions
        self.is_main_task = False

    def compose(self) -> ComposeResult:
        yield Label(str(self.task_id))
        yield Label(self.task_name, id="task_name_label")
        yield Label(
            f"󱎫 0 completed of 󱎫 {self.total_sessions}", classes="task_sessions"
        )


class TaskList(ListView):
    app: "DorotuiApp"

    BINDINGS = [
        ("ctrl+d", "erase_all_tasks", "Erase all tasks"),
        ("D", "delete_one_task", "Delete selected task"),
        ("ctrl+t", "create_task", "Create Task"),
    ]

    def on_mount(self) -> None:
        sessions = load_sessions()
        list_items = []
        for data in sessions:
            list_items.append(Task(data["id"], data["name"], data["total_sessions"]))
        self.extend(list_items)

    def on_list_view_selected(self, selected: ListView.Selected) -> None:
        new_config = self.app.config
        selected_item_id = cast(Task, selected.item).task_id
        selected_item_name = cast(Task, selected.item).task_name

        new_config["current_task"]["id"] = selected_item_id
        new_config["current_task"]["name"] = selected_item_name
        save_config(new_config)

    def action_erase_all_tasks(self) -> None:
        self.clear()
        erase_all_data()

    def action_delete_one_task(self) -> None:
        selected_task = cast(Task, self.highlighted_child)
        if selected_task:
            self.pop()
            delete_one_task(selected_task.task_id)

    def action_create_task(self):
        def handle_new_task(new_task: TaskType | None) -> None:
            if new_task:
                new_task_dict: TaskType = {
                    "id": new_task["id"],
                    "name": new_task["name"],
                    "total_sessions": new_task["total_sessions"],
                    "completed_sessions": 0,
                }
                self.append(
                    Task(new_task["id"], new_task["name"], new_task["total_sessions"])
                )
                save_session(new_task_dict)

        self.app.push_screen(CreateTaskModal(), handle_new_task)


class TasksScreen(Screen):
    CSS_PATH = "../styles/tasks.tcss"

    def on_mount(self) -> None:
        self.title = " Tasks"

    def compose(self) -> ComposeResult:
        yield CHeader()
        with Center():
            yield TaskList()
        yield Footer()
