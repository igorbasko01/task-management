import unittest

from task_cli.task import TaskPriority


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

class TaskTests(unittest.TestCase):
    pass    