#!/usr/bin/env python3
import os

import pkg_resources
import typer

from legl_dev.command import Command, Steps

app = typer.Typer(invoke_without_command=True)

os.environ["COMPOSE_DOCKER_CLI_BUILD"] = "1"
os.environ["DOCKER_BUILDKIT"] = "1"


@app.command(help="Start the dev enviroment")
def start():
    steps = Steps()
    steps.add(
        Command(
            command="docker compose up",
        )
    )
    steps.run()


@app.command(help="Rebuild the local enviroment")
def build(
    cache: bool = typer.Option(True, help="Drop the database and create a fresh one"),
) -> None:

    extra_args = f"{'' if cache else '--no-cache'} "
    steps = Steps(
        steps=[
            Command(
                command=f"docker compose build {extra_args}",
            ),
        ],
    )
    steps.add(
        [
            Command(command=f"docker compose up -d"),
            Command(command=(f"docker compose exec backend python manage.py migrate")),
            Command(
                command=(
                    f"docker compose exec backend python manage.py flush --noinput"
                )
            ),
            Command(
                command=(f"docker compose exec backend python manage.py run_factories")
            ),
            Command(
                command=(f"docker compose exec backend python manage.py seed_emails")
            ),
            Command(command=f"docker compose stop"),
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
                    f"docker compose "
                    "exec backend pytest "
                    "--html=unit_test_results.html "
                    f"{extra_args} {path}"
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
            Command(command=(f"isort . --profile black --line-length 99")),
            Command(command=(f"black . --line-length 99")),
            Command(command=("yarn format:prettier")),
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
                command=f"docker compose exec frontend yarn run cypress open",
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
            Command(
                command=(
                    f"docker compose "
                    "exec backend python manage.py makemigrations --merge"
                )
            ),
        )
    if make:
        steps.add(
            (
                Command(
                    command=(
                        f"docker compose "
                        "exec backend python manage.py makemigrations"
                    )
                )
            ),
        )
    if run:
        steps.add(
            Command(command=(f"docker compose exec backend python manage.py migrate")),
        )
    steps.run()


@app.command(help="Clean out and create new factories")
def factories(
    emails: bool = typer.Option(True, help="Generate factory emails"),
):

    steps = Steps(
        steps=[
            Command(
                command=(
                    f"docker compose exec backend python manage.py flush --noinput"
                )
            ),
            Command(
                command=(f"docker compose exec backend python manage.py run_factories")
            ),
        ],
    )
    if emails:
        steps.add(
            Command(
                command=(f"docker compose exec backend python manage.py seed_emails")
            ),
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

    steps = Steps(
        steps=[
            Command(command=(f"docker compose exec frontend yarn run test")),
            Command(
                command="open js-test-results/index.html",
            ),
        ]
    )
    steps.run()


@app.callback()
def main(version: bool = False):
    if version:
        typer.echo(f"v{pkg_resources.require('legl_dev')[0].version}")
        raise typer.Exit()


if __name__ == "__main__":
    app()
