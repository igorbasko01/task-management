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


@cli.command()
@click.argument("task_id")
@click.argument("priority")
def update_priority(task_id, priority):
    """Update task priority"""
    manager = TaskManager()
    manager.update_task_priority(task_id, priority)
    click.echo(f"🔝 Updated priority for task {task_id}")


@cli.command()
@click.argument("task_id")
@click.argument("category")
def update_category(task_id, category):
    """Update task category"""
    manager = TaskManager()
    manager.update_task_category(task_id, category)
    click.echo(f"📦 Updated category for task {task_id}")


@cli.command()
@click.option("--board", default="Backlog", help="Board name")
@click.option("--priority", default="Medium", help="Priority level")
@click.option("--category", default="Feature", help="Category name")
def list_tasks(board, priority, category):
    """List tasks based on board, priority, and category"""
    manager = TaskManager()
    tasks = manager.list_tasks(board=board, priority=priority, category=category)
    for task in tasks:
        click.echo(task)


if __name__ == "__main__":
    cli()
