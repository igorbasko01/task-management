from pathlib import Path

from task_cli.task import Task


class TaskManager:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.workspace = self.root_dir / ".tasks"
        self.tasks_dir = self.workspace / "tasks"
        self.task_counter_file = self.workspace / ".task_counter"
    
    def init_workspace(self):
        self.workspace.mkdir(exist_ok=True)
        self.tasks_dir.mkdir(exist_ok=True)
        self.task_counter_file.touch(exist_ok=True)
        with self.task_counter_file.open("w") as f:
            f.write("0")

    def create_task(self, title: str, category: str, owner: str):
        with self.task_counter_file.open("r+") as f:
            counter = int(f.read())
            f.seek(0)
            f.write(str(counter + 1))
            f.truncate()
        task = Task(counter + 1, title, "", 1, category, owner)
        task_file = self.tasks_dir / f"TASK-{task.task_id}.md"
        with task_file.open("w") as f:
            f.write(task.to_string())

    def move_task(self, task_id: int, board: str):
        task_file = self.tasks_dir / f"TASK-{task_id}.md"
        try:
            task_content = task_file.read_text()
        except FileNotFoundError:
            raise ValueError(f"Task {task_id} not found")
        task = Task.from_string(task_content)
        task.move_to_board(board)
        with task_file.open("w") as f:
            f.write(task.to_string())