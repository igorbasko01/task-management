import click

from task_cli.task import Task

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
@click.argument("title")
@click.option("--category", default="Feature", help="Task category")
@click.option("--owner", default="", help="Task owner")
def create(title, category, owner):
    """Create a new task"""
    manager = TaskManager()
    task_id = manager.create_task(title, category, owner)
    click.echo(f"✨ Task created: {task_id}")


@cli.command()
@click.argument("task_id")
@click.argument("to_board")
def move(task_id, to_board):
    """Move a task to a different board"""
    manager = TaskManager()
    task = manager.move_task(task_id, to_board)
    click.echo(f"➡️ Moved task {task.task_id} - {task.title} to {task.board.name}")


@cli.command()
@click.argument("task_id")
@click.option("--priority", default=None, help="Priority level")
@click.option("--category", default=None, help="Category name")
def update(task_id, priority, category):
    """Update task priority"""
    manager = TaskManager()
    if priority:
        manager.update_task_priority(task_id, priority)
        click.echo(f"🔝 Updated priority for task {task_id}")
    if category:
        manager.update_task_category(task_id, category)
        click.echo(f"🏷 Updated category for task {task_id}")


@cli.command()
@click.option("--board", default=None, help="Board name")
@click.option("--priority", default=None, help="Priority level")
@click.option("--category", default=None, help="Category name")
def list(board, priority, category):
    """List tasks based on board, priority, and category"""
    manager = TaskManager()
    tasks = manager.list_tasks(board=board, priority=priority, category=category)
    for task in tasks:
        click.echo(task)


@cli.command()
@click.argument("task_id")
def delete(task_id):
    """Delete a task"""
    manager = TaskManager()
    task_title = manager.delete_task(task_id)
    click.echo(f"🗑 Deleted task {task_title}")


@cli.command()
@click.argument("task_id")
@click.option("--editor", default="code", help="Editor to use")
def edit(task_id, editor):
    """Edit a task"""
    manager = TaskManager()
    task_path = manager.task_location(task_id)
    click.edit(filename=task_path, editor=editor)


if __name__ == "__main__":
    cli()
