#!/usr/bin/env python3
from os import environ

import typer

from legl_dev.command import Command, Steps

app = typer.Typer()


def docker_command(mutagen):
    if mutagen:
        return "mutagen-compose"
    return "docker compose"


@app.command(help="Start the dev enviroment")
def start(
    mutagen: bool = typer.Option(False, help="Run docker with Mutagen"),
    https: bool = typer.Option(False, help="Run server in HTTPS mode"),
    worker: bool = typer.Option(False, help="Run server with worker"),
    webpack: bool = typer.Option(True, help="Run server with webpack transpiller"),
):

    steps = Steps(concurrent=True)
    if https:
        environ["HOST_SCHEME"] = "https"
        environ["DEV_LOCAL_INSTALLED_APPS"] = '["sslserver"]'
        steps.add(
            Command(
                command=f"{docker_command(mutagen)} exec backend python manage.py runsslserver 0.0.0.0:443",
            )
        )
    else:
        environ.pop("HOST_SCHEME", None)
        environ.pop("DEV_LOCAL_INSTALLED_APPS", None)
        steps.add(
            Command(
                command=f"{docker_command(mutagen)} up backend",
            )
        )
    if worker:
        environ.pop("CELERY_TASK_ALWAYS_EAGER", "False")
        environ["CELERY_TASK_ALWAYS_EAGER"] = "False"
        steps.add(
            [
                Command(
                    command="rabbitmq-server",
                ),
                Command(
                    command="pm2 start ./legl_dev/pm2.config.js",
                ),
                Command(
                    command="pm2 log",
                ),
                Command(
                    command="rabbitmq-diagnostics log_tail_stream",
                ),
            ]
        )
    else:
        environ.pop("CELERY_TASK_ALWAYS_EAGER", None)

    if webpack:
        steps.add(
            Command(
                command=f"{docker_command(mutagen)} up frontend",
            )
        )

    steps.run()


@app.command(help="Rebuild the local enviroment")
def build(
    mutagen: bool = typer.Option(False, help="Run docker with Mutagen"),
    cache: bool = typer.Option(True, help="Drop the database and create a fresh one"),
) -> None:

    extra_args = f"{'' if cache else '--no-cache'} "
    steps = Steps(
        steps=[
            Command(
                command=f"{docker_command(mutagen)} build {extra_args}",
            ),
        ],
    )
    steps.add(
        [
            Command(command=f"{docker_command(mutagen)} up -d"),
            Command(
                command=f"{docker_command(mutagen)} exec backend python manage.py migrate",
            ),
            Command(
                command=f"{docker_command(mutagen)} exec backend python manage.py flush --noinput",
            ),
            Command(
                command=f"{docker_command(mutagen)} exec backend python manage.py run_factories",
            ),
            Command(
                command=f"{docker_command(mutagen)} exec backend python manage.py seed_emails",
            ),
            Command(command=f"{docker_command(mutagen)} stop"),
        ]
    )
    steps.run()

    print("Build complete 🚀")


@app.command(help="Run the local pytest unit tests")
def pytest(
    mutagen: bool = typer.Option(False, help="Run docker with Mutagen"),
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
    gui: bool = typer.Option(
        True,
        help="Toggle the output gui",
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
                command=f"{docker_command(mutagen)} exec backend pytest --html=unit_test_results.html {extra_args} {path}",
            ),
        ]
    )
    if gui:
        steps.add(
            Command(
                command=f"open ./unit_test_results.html",
            )
        )

    if snapshot_update:
        steps.add(
            Command(
                command=f"{docker_command(mutagen)} exec backend black .",
            )
        )
    steps.run()


@app.command(help="Format the code with isort, black and prettier")
def format(
    mutagen: bool = typer.Option(False, help="Run docker with Mutagen"),
    push: bool = typer.Option(False, help="Also push the changes to the repo"),
):

    steps = Steps(
        steps=[
            Command(
                command=f"{docker_command(mutagen)} exec backend isort .",
            ),
            Command(
                command=f"{docker_command(mutagen)} exec backend black .",
            ),
            Command(
                command=f"{docker_command(mutagen)} exec frontend yarn run format:prettier",
            ),
        ]
    )
    if push:
        steps.add(
            [
                Command(
                    command="git stage .",
                ),
                Command(
                    command='git commit -m "formatting"',
                ),
                Command(
                    log_file="git_push", desc="pushing changes", command="git push"
                ),
            ]
        )
    steps.run()


@app.command(help="Open Cypress e2e tests")
def cypress(mutagen: bool = typer.Option(False, help="Run docker with Mutagen")):

    steps = Steps(
        steps=[
            Command(
                command=f"{docker_command(mutagen)} exec frontend yarn run cypress open",
            )
        ]
    )
    steps.run()


@app.command(help="Create and run migrations")
def migrate(
    mutagen: bool = typer.Option(False, help="Run docker with Mutagen"),
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
                command=f"{docker_command(mutagen)} exec backend python manage.py makemigrations --merge",
            ),
        )
    if make:
        steps.add(
            Command(
                command=f"{docker_command(mutagen)} exec backend python manage.py makemigrations",
            ),
        )
    if run:
        steps.add(
            Command(
                command=f"{docker_command(mutagen)} exec backend python manage.py migrate",
            ),
        )
    steps.add(
        Command(
            command=f"{docker_command(mutagen)} exec backend black .",
        ),
    )
    steps.run()


@app.command(help="Clean out and create new factories")
def factories(
    mutagen: bool = typer.Option(False, help="Run docker with Mutagen"),
    emails: bool = typer.Option(True, help="Generate factory emails"),
):

    steps = Steps(
        steps=[
            Command(
                command=f"{docker_command(mutagen)} exec backend python manage.py flush --noinput",
            ),
            Command(
                command=f"{docker_command(mutagen)} exec backend python manage.py run_factories",
            ),
        ],
    )
    if emails:
        steps.add(
            Command(
                command=f"{docker_command(mutagen)} exec backend python manage.py seed_emails",
            ),
        )
    steps.run()


@app.command(help="Cleans out git branches")
def gitclean():
    steps = Steps(
        steps=[
            Command(
                command='git branch --merged | egrep -v "(^\\*|master|dev)" | xargs git branch -d',
                shell=True,
            ),
        ]
    )
    steps.run()


@app.command(help="Run JS unit tests")
def jstest(
    mutagen: bool = typer.Option(False, help="Run docker with Mutagen"),
):

    steps = Steps(
        steps=[
            Command(
                command=f"{docker_command(mutagen)} exec frontend yarn run test",
            ),
            Command(
                command="open js-test-results/index.html",
            ),
        ]
    )
    steps.run()


if __name__ == "__main__":
    app()
