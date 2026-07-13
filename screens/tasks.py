from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import Screen
from textual.widgets import Footer, Label, ListItem, ListView

from data import TaskType, load_sessions, save_session
from widgets.header import CHeader


class Task(ListItem):
    def __init__(self, task_id: str,task_name: str, total_timer: int):
        super().__init__()
        self.task_id = task_id
        self.task_name = task_name
        self.total_timer = total_timer

    def compose(self) -> ComposeResult:
        yield Label(str(self.task_id))
        yield Label(self.task_name, classes="task_name")
        yield Label(f'󱎫 0 completed of 󱎫 {self.total_timer}', classes="task_sessions")

class TaskList(ListView):
    saved_data:list[TaskType] = load_sessions()

    def on_list_view_selected(self) -> None:
        is_saved = save_session({"id": "123","name":"Estudio Diario","completed_sessions": 0, "total_sessions": 10})
        if is_saved:
            self.saved_data = load_sessions()


    def compose(self) -> ComposeResult:
        if len(self.saved_data) > 0:
            for task in self.saved_data:
                yield Task(task["id"],task["name"],task["total_sessions"])
        else:
            yield ListItem(Label('No Tasks'))

class TasksScreen(Screen):
    CSS_PATH="../styles/tasks.tcss"
    
    def on_mount(self) -> None:
        self.title = ' Tasks'

    def compose(self) -> ComposeResult:
        yield CHeader()
        with Center():
            yield TaskList()
        yield Footer()
