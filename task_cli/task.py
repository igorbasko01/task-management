from dataclasses import dataclass
from datetime import datetime

import frontmatter


@dataclass
class TaskHistory:
    timestamp: datetime
    action: str

    @classmethod
    def from_string(cls, history_entry: str):
        timestamp_str, action = history_entry.split(" - ")
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return cls(timestamp=timestamp, action=action)

    def to_string(self):
        return f"{self.timestamp.strftime("%Y-%m-%d %H:%M:%S")} - {self.action}"


@dataclass
class TaskPriority:
    name: str
    numeric_value: int  # Lower value means higher priority

    _value_map = {
        0: "High",
        1: "Medium",
        2: "Low"
    }

    @classmethod
    def from_numeric_value(cls, value: int):
        lowest_priority = sorted(list(cls._value_map.keys()))[-1]
        # If the value is not in the map, set the priority to the lowest priority
        name = cls._value_map.get(value, cls._value_map[lowest_priority])
        return cls(name=name, numeric_value=value)
    
    @classmethod
    def from_name(cls, name: str):
        for value, priority in cls._value_map.items():
            if priority == name:
                return cls(name=priority, numeric_value=value)
        raise ValueError(f"Invalid priority name: {name}")



class Task:

    _categories = ["Bug", "Feature", "Documentation", "Maintenance", "UI/UX", "Security"]
    _boards = ["Backlog", "In Progress", "Done"]

    _task_template = """---
id: TASK-{task_id}
title: {title}
created: {created}
priority: {priority}
category: {category}
owner: {owner}
board: {board}
---
            
## Description
{description}
            
## Notes
{notes}
            
## History
{created} - Created
"""

    def __init__(self, 
                 task_id: int, 
                 title: str, 
                 description: str, 
                 priority: int, 
                 category: str, 
                 owner: str,
                 created: datetime, 
                 board: str = "Backlog",
                 notes: str = "",
                 history: TaskHistory = []):
        self.task_id: int = task_id
        self.title: str = title
        self.created: datetime = created or datetime.now()
        self.priority: TaskPriority = TaskPriority.from_numeric_value(priority)
        self.category: str = self._validate_category(category)
        self.owner: str = owner
        self.board: str = self._validate_board(board)
        self.description: str = description
        self.notes: str = notes
        self.history: TaskHistory = history

    @classmethod
    def from_string(cls, task_str: str):
        # Read front matter
        task = frontmatter.loads(task_str)
        if not task.metadata:
            raise ValueError("Invalid task front matter")
        # extract description and notes
        description = task.content.split("## Description")[1].split("## Notes")[0].strip()
        notes = task.content.split("## Notes")[1].split("## History")[0].strip()
        # extract history
        history = task.content.split("## History")[1].strip()
        history = [TaskHistory.from_string(entry) for entry in history.split("\n")]
        # extract task id
        task_id = int(task.metadata["id"].split("-")[1])
        # extract priority
        priority = TaskPriority.from_name(task.metadata["priority"])
        created = task.metadata["created"]
        # Create Task object
        return cls(
            task_id=task_id,
            title=task.metadata["title"],
            description=description,
            priority=priority.numeric_value,
            category=task.metadata["category"],
            created=created,
            owner=task.metadata["owner"],
            board=task.metadata["board"],
            notes=notes,
            history=history
        )

    def _validate_category(self, category: str) -> str:
        if category not in self._categories:
            raise ValueError(f"Invalid category: {category}, allowed categories: {self._categories}")
        return category
    
    def _validate_board(self, board: str) -> str:
        if board not in self._boards:
            raise ValueError(f"Invalid board: {board}, allowed boards: {self._boards}")
        return board