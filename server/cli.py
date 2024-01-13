import click
from pathlib import Path


@click.group()
def cli():
    """FastAPI Project Management"""


@click.command("startapp")
@click.option("-r", "--root-dir", default=".", help="Generate app in this directory")
@click.argument("name")
def start_app(root_dir, name):
    """Create a new FastAPI app"""
    root_dir = Path(root_dir) / name
    root_dir.mkdir(parents=True, exist_ok=True)
    package_path = root_dir / "__init__.py"
    package_path.touch()
    for file in ["models", "controller", "service", "repository", "test"]:
        file_path = package_path.parent / f"{file}.py"
        file_path.touch()
    print("App has been created.")


@click.command("runserver")
@click.option("-h", "--host", default="127.0.0.1", help="Host address")
@click.option("-p", "--port", default=8000, help="Port number")
@click.option(
    "--reload/--no-reload", default=True, help="Enable/disable auto-reloading"
)
@click.argument("app_module", type=Path)
def runserver(host: str, port: int, reload: bool, app_module: Path):
    """Start the FastAPI server"""
    import uvicorn

    uvicorn.run(str(app_module), host=host, port=port, reload=reload)


def validate_action(ctx, param, value):
    if value not in ["lint", "format"]:
        raise click.BadParameter(f"Action must be 'lint' or 'format', but got '{value}'.")
    return value


@click.command("codestyle")
@click.option("-a", "--act", default="format", callback=validate_action, help="Actions is 'lint' or 'format'")
@click.option("-m", "--module", default=".", help="Directory path")
def format_code(act, module):
    import subprocess
    subprocess.run(["ruff", act, module])


cli.add_command(start_app)
cli.add_command(runserver)
cli.add_command(format_code)

if __name__ == '__main__':
    cli()