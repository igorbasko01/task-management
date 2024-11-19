import click

from .task_manager import TaskManager


@click.group()
def cli():
    """Task management system"""
    pass


@cli.command()
def init():
    """Initialize the task management system"""
    manager = TaskManager()
    manager.init_workspace()


@cli.command()
@click.option("--title", required=True, help="Task title")
@click.option("--description", required=True, help="Task description")
@click.option("--priority", default="Medium", help="Task priority")
@click.option("--category", default="Feature", help="Task category")
@click.option("--owner", default="", help="Task owner")
def create(title, description, priority, category, owner):
    """Create a new task"""
    manager = TaskManager()
    task_id = manager.create_task(title, description, priority, category, owner)
    click.echo(f"✨ Task created: {task_id}")


@cli.command()
@click.argument("task_id")
@click.argument("to_board")
def move(task_id, to_board):
    """Move a task to a different board"""
    manager = TaskManager()
    manager.move_task(task_id, to_board)
    click.echo(f"➡️ Moved task {task_id} to {to_board}")


if __name__ == "__main__":
    cli()
