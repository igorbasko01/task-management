from dataclasses import dataclass
from datetime import datetime


@dataclass
class TaskHistory:
    timestamp: datetime
    action: str


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
        lowest_priority = sorted(cls._value_map.keys())[-1]
        # If the value is not in the map, set the priority to the lowest priority
        name = cls._value_map.get(value, cls._value_map[lowest_priority])
        return cls(name=name, numeric_value=value)



class Task:

    _task_template = """---
id: TASK-{task_id}
title: {title}
created: {created}
priority: {priority}
category: {category}
owner: {owner}
board: {status}
---
            
## Description
{description}
            
## Notes
{notes}
            
## History
- {created} - Created
"""

    def __init__(self, 
                 task_id: int, 
                 title: str, 
                 description: str, 
                 priority: str, 
                 category: str, 
                 owner: str, 
                 board: str = "Backlog"):
        self.task_id: int = task_id
        self.title: str = title
        self.created: datetime = datetime.now()
        self.priority: TaskPriority = priority
        self.category: str = category
        self.owner: str = owner
        self.board: str = board
        self.description: str = description
        self.notes: str = ""
        self.history: TaskHistory = []