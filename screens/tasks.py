import uuid

from textual.app import ComposeResult
from textual.containers import (Center, CenterMiddle, HorizontalGroup,
                                VerticalGroup)
from textual.reactive import reactive
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, Footer, Input, Label, ListItem, ListView

from data import (TaskType, delete_one_task, erase_all_data, load_sessions,
                  save_session)
from widgets.header import CHeader


class CreateTaskScreen(ModalScreen[list]):
    def compose(self) -> ComposeResult:
        with CenterMiddle():
            yield VerticalGroup(
                Label("Task name:"),
                Input(placeholder="Daily study", type="text", id="input_task_name"),
                Label("Total sessions:"),
                Input(placeholder="10", type="integer", id="input_total_sessions"),
                HorizontalGroup(
                    Button("Create", variant="default", id="button_create_task"),
                    Button("Cancel", variant="primary", id="button_cancel"), id="button_box"),
                id="dialog_create_task")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "button_create_task":
            task_name = self.query_exactly_one('#input_task_name', Input).value
            total_sessions = self.query_exactly_one('#input_total_sessions', Input).value
            new_id = uuid.uuid4()

            if task_name and total_sessions:
                task:TaskType = {
                    "id" : str(new_id)[0:8],
                    "name": task_name,
                    "completed_sessions": 0,
                    "total_sessions": int(total_sessions)
                }

                new_session = save_session(task)
                self.dismiss(new_session)
            else:
                self.notify('Fill the required inputs')
        else:
            self.app.pop_screen()


class Task(ListItem):
    def __init__(self, task_id: str,task_name: str, total_timer: int):
        super().__init__()
        self.task_id = task_id
        self.task_name = task_name
        self.total_timer = total_timer
        self.is_main_task = False

    def compose(self) -> ComposeResult:
        yield Label(str(self.task_id))
        yield Label(self.task_name)
        yield Label(f'󱎫 0 completed of 󱎫 {self.total_timer}', classes="task_sessions")

class TaskList(ListView):
    BINDINGS = [('ctrl+d','erase_all_tasks','Erase all tasks'),
                ('n','check_current_task','Check current main task'),
                ('D','delete_one_task','Delete selected task'),
                ]

    saved_data:reactive[list] = reactive(load_sessions(), recompose=True)

    def on_list_view_selected(self,selected: ListView.Selected) -> None:
        TasksScreen.current_main_task = selected.item.task_id

    def action_check_current_task(self) -> None:
        self.notify(str(TasksScreen.current_main_task))

    def action_erase_all_tasks(self) -> None:
        erase_all_data()
        self.saved_data = []

    def action_delete_one_task(self) -> None:
        selected_task = self.highlighted_child
        if selected_task:
            new_data = delete_one_task(selected_task.task_id)
            if new_data:
                self.saved_data = new_data

    def compose(self) -> ComposeResult:
        if len(self.saved_data) > 0:
            for task in self.saved_data:
                yield Task(task["id"],task["name"],task["total_sessions"])
        else:
            yield ListItem(Label('No Tasks'))


class TasksScreen(Screen):
    CSS_PATH="../styles/tasks.tcss"
    BINDINGS = [('ctrl+t','create_task','Create Task')]

    current_main_task: str | None = None

    def action_create_task(self):
        def update_saved_data(new_data: list[TaskType] | None) -> None:
            if new_data is not None:
                self.query_exactly_one(TaskList).saved_data = new_data

        self.app.push_screen(CreateTaskScreen(), update_saved_data)

    def on_mount(self) -> None:
        self.title = ' Tasks'

    def compose(self) -> ComposeResult:
        yield CHeader()
        with Center():
            yield TaskList()
        yield Footer()
