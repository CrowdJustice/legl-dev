#!/usr/bin/env python3
import json
import os
from typing import Optional

import pkg_resources
import requests
import typer
from legl_dev.command import Command, Steps

app = typer.Typer(invoke_without_command=True)
docker_cmd = "docker compose"
exec_cmd = f"{docker_cmd} exec server"
django_cmd = f"{exec_cmd} python manage.py"
os.environ["COMPOSE_DOCKER_CLI_BUILD"] = "1"
os.environ["DOCKER_BUILDKIT"] = "1"


@app.command(help="Start the dev environment")
def start(verbose: bool = typer.Option(True, help="Run in verbose mode")):
    steps = Steps()
    steps.add(
        Command(
            command=f"{docker_cmd} up {'' if verbose else '-d'}",
        )
    )
    steps.run()


@app.command(help="Start the dev environment")
def logs():
    steps = Steps()
    steps.add(
        Command(
            command=f"{docker_cmd} logs -f",
        )
    )
    steps.run()


@app.command(help="Rebuild the local environment")
def build(
    cache: bool = typer.Option(True, help="Drop the database and create a fresh one"),
) -> None:

    extra_args = f"{'' if cache else '--no-cache'}"
    steps = Steps(
        steps=[
            Command(
                command=f"{docker_cmd} build {extra_args}",
            ),
        ],
    )
    steps.add(
        [
            Command(command=f"{docker_cmd} up -d"),
            Command(command=f"{django_cmd} migrate"),
            Command(command=f"{docker_cmd} stop database"),
            Command(command=f"{docker_cmd} rm -f database"),
            Command(command=f"{docker_cmd} up database -d"),
            Command(command=f"{django_cmd} migrate"),
            Command(command=f"{django_cmd} run_factories"),
            Command(command=f"{django_cmd} seed_emails"),
            Command(command=f"{docker_cmd} stop"),
        ]
    )
    steps.run()


@app.command(help="Run the local pytest unit tests")
def pytest(
    full_diff: bool = typer.Option(
        False,
        help="Show full diff in errors",
    ),
    create_db: bool = typer.Option(
        False,
        help="Recreates the test database",
    ),
    last_failed: bool = typer.Option(
        False,
        help="Run the last failed tests",
    ),
    warnings: bool = typer.Option(
        False,
        help="Toggle warnings in output",
    ),
    snapshot_update: bool = typer.Option(
        False,
        help="update snapshots",
    ),
    show_capture: bool = typer.Option(
        False,
        help="show captured stdout",
    ),
    parallel: bool = typer.Option(
        False,
        help="run tests in parallel",
    ),
    all_logs: bool = typer.Option(
        False,
        help="show print outputs instead of just logs",
    ),
    path: str = typer.Argument(
        "",
        help='path for specific test in the format "<file path>::<class name>::<function name>"',
    ),
):

    extra_args = (
        f"{'--create-db' if create_db else ''} "
        f"{'-vv' if full_diff else ''} "
        f"{'--lf' if last_failed else ''} "
        f"{'' if warnings else '--disable-warnings'} "
        f"{'' if all_logs else '--show-capture=log'} "
        f"{'--snapshot-update' if snapshot_update else ''} "
        f"{'--show-capture=stdout' if show_capture else ''} "
        f"{'-n auto --dist loadscope' if parallel else ''} "
    )
    steps = Steps(
        steps=[
            Command(
                command=(
                    f"{docker_cmd} "
                    "run --rm server pytest "
                    "--html=unit_test_results.html "
                    f"{extra_args} /code/{path}"
                )
            ),
        ]
    )
    steps.run()


@app.command(help="Format the code with isort, black and prettier")
def format(
    push: bool = typer.Option(False, help="Also push the changes to the repo"),
):

    steps = Steps(
        steps=[
            Command(command=f"isort . --profile black"),
            Command(command=f"black ."),
            Command(command="yarn format:prettier"),
        ]
    )
    if push:
        steps.add(
            [
                Command(
                    command="git stage .",
                ),
                Command(
                    command="git commit -m formatting",
                ),
                Command(command="git push"),
            ]
        )
    steps.run()


@app.command(help="Open Cypress e2e tests")
def cypress():
    steps = Steps(
        steps=[
            Command(
                command=f"yarn run cypress open",
            )
        ]
    )
    steps.run()


@app.command(help="Create and run migrations")
def migrate(
    merge: bool = typer.Option(False, help="Run a migration merge first"),
    make: bool = typer.Option(False, help="Run makemigrations before migrating"),
    run: bool = typer.Option(
        True, help="use --no-run to prevent migrations from running"
    ),
):

    steps = Steps()
    if merge:
        steps.add(
            Command(command=f"{django_cmd} makemigrations --merge"),
        )
    if make:
        steps.add(
            (Command(command=f"{django_cmd} makemigrations")),
        )
    if run:
        steps.add(
            Command(command=f"{django_cmd} migrate"),
        )
    steps.run()


@app.command(help="Clean out and create new factories")
def factories(
    emails: bool = typer.Option(True, help="Generate factory emails"),
):

    steps = Steps(
        steps=[
            Command(command=f"{django_cmd} run_factories"),
        ],
    )
    if emails:
        steps.add(
            Command(command=f"{django_cmd} seed_emails"),
        )
    steps.run()


@app.command(help="Cleans out git branches")
def gitclean():
    steps = Steps(
        steps=[
            Command(
                command=(
                    "git branch --merged | "
                    'egrep -v "(^\\*|master|dev)" | '
                    "xargs git branch -d"
                ),
                shell=True,
            ),
        ]
    )
    steps.run()


@app.command(help="Run JS unit tests")
def jstest():

    steps = Steps(steps=[Command(command=(f"yarn run test"))])
    steps.run()


@app.command(help="Install packages to the dev environment")
def install(
    package: Optional[str] = typer.Argument(
        default="", help="Name of the package you would like to install"
    ),
    pip: bool = typer.Option(default=False, help="Install package using pip"),
    yarn: bool = typer.Option(default=False, help="Install package using yarn"),
    self: bool = typer.Option(
        default=False,
        help="Reinstall legl-dev, can be used with --upgrade to on update current install",
    ),
    version: str = typer.Option(
        default="main", help="specify version of legl-dev to install"
    ),
    upgrade: bool = typer.Option(
        default=False, help="upgrade existing package instead of installing"
    ),
):
    steps = Steps()
    if pip:
        steps.add(
            [
                Command(
                    command=(
                        f"{exec_cmd} pip install {'--upgrade' if upgrade else ''} {package}"
                    )
                ),
                Command(
                    command=(
                        f"{exec_cmd} pip freeze | grep {package} >> requirements.txt"
                    ),
                    shell=True,
                ),
            ]
        )

    if yarn:
        steps.add(
            Command(command=(f"{exec_cmd} yarn {'up' if upgrade else 'add'} {package}"))
        )

    if self:
        if upgrade:
            steps.add(Command(command=f"pip install --upgrade legl-dev"))
        else:
            steps.add(
                [
                    Command(command=("pip uninstall legl-dev -y")),
                    Command(
                        command=(
                            f"pip install git+https://github.com/CrowdJustice/legl-dev.git@{version}"
                        )
                    ),
                ]
            )

    steps.run()


@app.command(help="Remote into a container")
def shell():
    steps = Steps()
    steps.add(Command(command=f"{exec_cmd} bash"))
    steps.run()


@app.callback()
def main(version: bool = False):
    response = requests.get(
        url="https://api.github.com/repos/crowdjustice/legl-dev/releases",
        headers={"Accept": "application/vnd.github.v3+json"},
    )
    releases = response.json()
    latest_vesrion = pkg_resources.parse_version(releases[0]["tag_name"])
    current_version = pkg_resources.parse_version(
        pkg_resources.require("legl_dev")[0].version
    )

    if latest_vesrion > current_version:
        update = typer.confirm(
            f"A newer version ({latest_vesrion}) of legl-dev is availible, would you like to update?"
        )
        if update:
            command = Command(command=f"pip install --upgrade legl-dev")
            command.run()

    if version:
        typer.echo(f"v{current_version}")
        raise typer.Exit()


if __name__ == "__main__":
    app()
