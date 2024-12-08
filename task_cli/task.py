from dataclasses import dataclass
from datetime import datetime
from typing import List

import frontmatter

from task_cli.board import Board
from task_cli.task_priority import TaskPriority


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
    

class Task:

    _categories = ["Bug", "Feature", "Documentation", "Maintenance", "UI/UX", "Security"]
    
    _boards = [
        Board("Backlog", "BL"), 
        Board("In Progress", "IP"), 
        Board("Done", "DN")
    ]

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
{history}
"""

    def __init__(self, 
                 task_id: int, 
                 title: str, 
                 description: str, 
                 priority: TaskPriority, 
                 category: str, 
                 owner: str,
                 created: datetime = None, 
                 board: str = "Backlog",
                 notes: str = "",
                 history: List[TaskHistory] = []):
        self.task_id: int = task_id
        self.title: str = title
        self.created: datetime = created or datetime.now()
        self._priority: TaskPriority = priority
        self._category: str = self._validate_category(category)
        self.owner: str = owner
        self._board: Board = self._validate_board(board)
        self.description: str = description
        self.notes: str = notes
        self.history: List[TaskHistory] = history or [TaskHistory(timestamp=self.created, action="Created")]

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
        history = [TaskHistory.from_string(entry) for entry in history.split("\n\n")]
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
            priority=priority,
            category=task.metadata["category"],
            created=created,
            owner=task.metadata["owner"],
            board=task.metadata["board"],
            notes=notes,
            history=history
        )
    
    def to_string(self):
        history = "\n\n".join([entry.to_string() for entry in self.history])
        return self._task_template.format(
            task_id=self.task_id,
            title=self.title,
            description=self.description,
            priority=self._priority.name,
            category=self._category,
            owner=self.owner,
            created=self.created.strftime("%Y-%m-%d %H:%M:%S"),
            board=self._board.name,
            notes=self.notes,
            history=history)
    
    @property
    def board(self):
        return self._board
    
    @property
    def priority(self):
        return self._priority
    
    @property
    def category(self):
        return self._category
    
    def move_to_board(self, to_board: str):
        self._board = self._validate_board(to_board)
        timestamp = datetime.now()
        self.history.append(TaskHistory(timestamp=timestamp, action=f"Moved to {self._board.name}"))

    def update_priority(self, priority: TaskPriority):
        self._priority = priority
        timestamp = datetime.now()
        self.history.append(TaskHistory(timestamp=timestamp, action=f"Priority updated to {self._priority.name}"))

    def update_category(self, category: str):
        self._category = self._validate_category(category)
        timestamp = datetime.now()
        self.history.append(TaskHistory(timestamp=timestamp, action=f"Category updated to {self._category}"))

    def _validate_category(self, category: str) -> str:
        if category not in self._categories:
            raise ValueError(f"Invalid category: {category}, allowed categories: {self._categories}")
        return category
    
    def _validate_board(self, board: str) -> Board:
        for _board in self._boards:
            if _board == board:
                return _board
        raise ValueError(f"Invalid board: {board}, allowed boards: {self._boards}")
    
    def __str__(self):
        return f"TASK-{self.task_id}: {self.title} ({self._priority.name}, {self._category}, {self._board.name})"