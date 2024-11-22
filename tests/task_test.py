from datetime import datetime
import unittest

from task_cli.task import TaskHistory, TaskPriority


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
    pass    