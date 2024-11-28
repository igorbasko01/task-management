import tempfile
import unittest

from task_cli.task_manager import TaskManager


class TaskManagerTests(unittest.TestCase):
    def test_init_workspace_if_doesnt_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            self.assertTrue(task_manager.workspace.exists())
            self.assertTrue(task_manager.tasks_dir.exists())
            self.assertTrue(task_manager.task_counter_file.exists())

    def test_init_workspace_should_initialize_counter_with_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            with task_manager.task_counter_file.open("r") as f:
                counter = f.read()
                self.assertEqual(counter, "0")

    def test_create_task_should_increment_counter(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            task_manager.create_task("Test Task", "Feature", "Test User")
            with task_manager.task_counter_file.open("r") as f:
                counter = f.read()
                self.assertEqual(counter, "1")

    def test_create_task_should_create_task_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_manager = TaskManager(tmp)
            task_manager.init_workspace()
            task_manager.create_task("Test Task", "Feature", "Test User")
            task_file = task_manager.tasks_dir / "TASK-1.md"
            self.assertTrue(task_file.exists())
        