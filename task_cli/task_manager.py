from pathlib import Path

from task_cli.task import Task
from task_cli.task_priority import PriorityLevel, TaskPriority


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

    def create_task(self, title: str, category: str, owner: str) -> int:
        with self.task_counter_file.open("r+") as f:
            counter = int(f.read())
            f.seek(0)
            f.write(str(counter + 1))
            f.truncate()
        task_id = counter + 1
        task = Task(task_id, title, "", TaskPriority(PriorityLevel.MEDIUM), category, owner)
        task_file = self.tasks_dir / f"{task.task_id}.md"
        with task_file.open("w") as f:
            f.write(task.to_string())
        return task.task_id

    def move_task(self, task_id: int, board: str) -> Task:
        task_file = self.tasks_dir / f"{Task.task_id_from_string(task_id)}.md"
        try:
            task_content = task_file.read_text()
        except FileNotFoundError:
            raise ValueError(f"Task {task_id} not found")
        task = Task.from_string(task_content)
        task.move_to_board(board)
        with task_file.open("w") as f:
            f.write(task.to_string())
        return task

    def update_task_priority(self, task_id: int, priority: str):
        task_file = self.tasks_dir / f"{Task.task_id_from_string(task_id)}.md"
        try:
            task_content = task_file.read_text()
        except FileNotFoundError:
            raise ValueError(f"Task {task_id} not found")
        task = Task.from_string(task_content)
        task.update_priority(TaskPriority.from_name(priority))
        with task_file.open("w") as f:
            f.write(task.to_string())

    def update_task_category(self, task_id: int, category: str):
        task_file = self.tasks_dir / f"{Task.task_id_from_string(task_id)}.md"
        try:
            task_content = task_file.read_text()
        except FileNotFoundError:
            raise ValueError(f"Task {task_id} not found")
        task = Task.from_string(task_content)
        task.update_category(category)
        with task_file.open("w") as f:
            f.write(task.to_string())

    def list_tasks(self, board: str = None, category: str = None, priority: str = None):
        tasks = []
        for task_file in self.tasks_dir.iterdir():
            task_content = task_file.read_text()
            task = Task.from_string(task_content)
            if board and task.board != board:
                continue
            if category and task._category != category:
                continue
            if priority and task._priority.name != priority:
                continue
            tasks.append(task)
        return tasks
    
    def delete_task(self, task_id: int):
        task_file = self.tasks_dir / f"{Task.task_id_from_string(task_id)}.md"
        try:
            task = Task.from_string(task_file.read_text())
            task_file.unlink()
            return task.task_id_with_title
        except FileNotFoundError:
            raise ValueError(f"Task {task_id} not found")