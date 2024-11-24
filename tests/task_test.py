from datetime import datetime
import unittest

from task_cli.task import Task, TaskHistory, TaskPriority


class TaskPriorityTests(unittest.TestCase):
    def test_priority_from_numeric_value_0(self):
        priority = TaskPriority.from_numeric_value(0)
        self.assertEqual(priority.name, "High")

    def test_priority_from_numeric_value_1(self):
        priority = TaskPriority.from_numeric_value(1)
        self.assertEqual(priority.name, "Medium")

    def test_priority_from_numeric_value_2(self):
        priority = TaskPriority.from_numeric_value(2)
        self.assertEqual(priority.name, "Low")

    def test_priority_from_numeric_value_invalid_set_priority_lowest(self):
        priority = TaskPriority.from_numeric_value(3)
        self.assertEqual(priority.name, "Low")


class TaskHistoryTests(unittest.TestCase):
    def test_history_to_string(self):
        history = TaskHistory(timestamp=datetime(2021, 1, 1, 12, 0, 1), action="Created")
        self.assertEqual(history.to_string(), "2021-01-01 12:00:01 - Created")

    def test_history_from_string(self):
        history = TaskHistory.from_string("2021-01-01 12:00:01 - Created")
        self.assertEqual(history.timestamp, datetime(2021, 1, 1, 12, 0, 1))
        self.assertEqual(history.action, "Created")

class TaskTests(unittest.TestCase):
    _valid_task_str = """---
id: TASK-1
title: Test Task
created: 2021-01-01 12:00:00
priority: High
category: Bug
owner: Test User
board: Backlog
---

## Description
This is a test task

## Notes
This is a note

## History
2021-01-01 12:00:00 - Created
2021-01-01 12:00:01 - Moved to In Progress
"""

    _invalid_frontmatter_task_str = """---
id: TASK-1
title: Test Task
created: 2021-01-01 12:00:00
priority: High
category: Bug
owner: Test User
board: Backlog
# missing closing frontmatter


## Description
This is a test task

## Notes
This is a note

## History
2021-01-01 12:00:00 - Created
"""

    _invalid_history_task_str = """---
id: TASK-1
title: Test Task
created: 2021-01-01 12:00:00
priority: High
category: Bug
owner: Test User
board: Backlog
---

## Description
This is a test task

## Notes
This is a note

## History
2021-01-01 12:00:00 - Created
12345 - Moved to In Progress
"""
    
    def test_task_from_string_valid(self):
        task = Task.from_string(self._valid_task_str)
        self.assertEqual(task.task_id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.created, datetime(2021, 1, 1, 12, 0, 0))
        self.assertEqual(task.priority.name, "High")
        self.assertEqual(task.category, "Bug")
        self.assertEqual(task.owner, "Test User")
        self.assertEqual(task.board, "Backlog")
        self.assertEqual(task.description, "This is a test task")
        self.assertEqual(task.notes, "This is a note")
        self.assertEqual(len(task.history), 2)
        self.assertEqual(task.history[0].to_string(), "2021-01-01 12:00:00 - Created")
        self.assertEqual(task.history[1].to_string(), "2021-01-01 12:00:01 - Moved to In Progress")

    def test_task_from_string_invalid_frontmatter(self):
        with self.assertRaises(ValueError):
            Task.from_string(self._invalid_frontmatter_task_str)

    def test_task_from_string_invalid_history(self):
        with self.assertRaises(ValueError):
            Task.from_string(self._invalid_history_task_str)

    def test_task_to_string_valid(self):
        task = Task.from_string(self._valid_task_str)
        task_str = task.to_string()
        self.assertEqual(task_str, self._valid_task_str)