from datetime import datetime
import unittest

from task_cli.board import Board
from task_cli.task import Task, TaskHistory
from task_cli.task_priority import TaskPriority


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
        self.assertEqual(task._task_id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.created, datetime(2021, 1, 1, 12, 0, 0))
        self.assertEqual(task._priority.name, "High")
        self.assertEqual(task._category, "Bug")
        self.assertEqual(task.owner, "Test User")
        self.assertEqual(task._board, Board("Backlog", "BL"))
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
    
    def test_task_created_adds_history(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User")
        self.assertEqual(len(task.history), 1)
        self.assertEqual(task.history[0], TaskHistory(timestamp=task.created, action="Created"))

    def test_task_move_to_backlog_board(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User", board="In Progress")
        task.move_to_board("Backlog")
        self.assertEqual(task._board, "Backlog")

    def test_task_move_to_backlog_board_adds_history(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User", board="In Progress")
        task.move_to_board("Backlog")
        self.assertEqual(len(task.history), 2)
        self.assertEqual(task.history[1].action, "Moved to Backlog")
        self.assertGreater(task.history[1].timestamp, task.created)

    def test_task_move_to_in_progress_board(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User")
        task.move_to_board("In Progress")
        self.assertEqual(task._board, "In Progress")

    def test_task_move_to_in_progress_board_adds_history(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User")
        task.move_to_board("In Progress")
        self.assertEqual(len(task.history), 2)
        self.assertEqual(task.history[1].action, "Moved to In Progress")
        self.assertGreater(task.history[1].timestamp, task.created)


    def test_task_move_to_done_board(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User", board="In Progress")
        task.move_to_board("Done")
        self.assertEqual(task._board, "Done")

    def test_task_move_to_done_board_adds_history(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User", board="In Progress")
        task.move_to_board("Done")
        self.assertEqual(len(task.history), 2)
        self.assertEqual(task.history[1].action, "Moved to Done")
        self.assertGreater(task.history[1].timestamp, task.created)

    def test_task_move_to_invalid_board_raises_exception(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User")
        with self.assertRaises(ValueError):
            task.move_to_board("Invalid Board")

    def test_task_update_priority_to_high(self):
        task = Task(1, "Test Task", "This is a test task", 1, "Bug", "Test User")
        task.update_priority(TaskPriority.from_numeric_value(0))
        self.assertEqual(task._priority.name, "High")

    def test_task_update_priority_to_high_adds_history(self):
        task = Task(1, "Test Task", "This is a test task", 1, "Bug", "Test User")
        task.update_priority(TaskPriority.from_numeric_value(0))
        self.assertEqual(len(task.history), 2)
        self.assertEqual(task.history[1].action, "Priority updated to High")
        self.assertGreater(task.history[1].timestamp, task.created)

    def test_task_update_priority_to_medium(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User")
        task.update_priority(TaskPriority.from_numeric_value(1))
        self.assertEqual(task._priority.name, "Medium")

    def test_task_update_priority_to_medium_adds_history(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User")
        task.update_priority(TaskPriority.from_numeric_value(1))
        self.assertEqual(len(task.history), 2)
        self.assertEqual(task.history[1].action, "Priority updated to Medium")
        self.assertGreater(task.history[1].timestamp, task.created)

    def test_task_update_priority_to_low(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User")
        task.update_priority(TaskPriority.from_numeric_value(2))
        self.assertEqual(task._priority.name, "Low")

    def test_task_update_priority_to_low_adds_history(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User")
        task.update_priority(TaskPriority.from_numeric_value(2))
        self.assertEqual(len(task.history), 2)
        self.assertEqual(task.history[1].action, "Priority updated to Low")
        self.assertGreater(task.history[1].timestamp, task.created)

    def test_task_update_priority_invalid_priority_raises_exception(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User")
        with self.assertRaises(ValueError):
            task.update_priority(TaskPriority.from_numeric_value(3))

    def test_task_update_category_valid(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User")
        task.update_category("Feature")
        self.assertEqual(task._category, "Feature")

    def test_task_update_category_valid_adds_history(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User")
        task.update_category("Feature")
        self.assertEqual(len(task.history), 2)
        self.assertEqual(task.history[1].action, "Category updated to Feature")
        self.assertGreater(task.history[1].timestamp, task.created)

    def test_task_update_category_invalid_category_raises_exception(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User")
        with self.assertRaises(ValueError):
            task.update_category("Invalid Category")

    def test_task_str(self):
        task = Task(1, "Test Task", "This is a test task", TaskPriority.from_numeric_value(0), "Bug", "Test User")
        self.assertEqual(str(task), "TASK-1: Test Task (High, Bug, Backlog)")

    def test_task_move_to_board_in_progress_through_acronym(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User")
        task.move_to_board("ip")
        self.assertEqual(task._board, "In Progress")

    def test_task_move_to_board_done_through_acronym(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User")
        task.move_to_board("dn")
        self.assertEqual(task._board, "Done")

    def test_task_move_to_board_backlog_through_acronym(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User", board="In Progress")
        task.move_to_board("bl")
        self.assertEqual(task._board, "Backlog")

    def test_task_move_to_board_invalid_acronym_raises_exception(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User")
        with self.assertRaises(ValueError):
            task.move_to_board("invalid")

    def test_task_move_to_board_acronym_history_uses_name(self):
        task = Task(1, "Test Task", "This is a test task", 0, "Bug", "Test User")
        task.move_to_board("ip")
        self.assertEqual(task.history[1].action, "Moved to In Progress")
