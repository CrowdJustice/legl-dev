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
    verbose: bool = typer.Option(True, help="Run the command in verbose mode"),
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
                desc="Starting django over SSL",
                log_file="start_django_ssl",
                verbose=verbose,
            )
        )
    else:
        environ.pop("HOST_SCHEME", None)
        environ.pop("DEV_LOCAL_INSTALLED_APPS", None)
        steps.add(
            Command(
                command=f"{docker_command(mutagen)} up backend",
                desc="Starting docker compose",
                log_file="start_docker_compose",
                verbose=verbose,
            )
        )
    if worker:
        environ.pop("CELERY_TASK_ALWAYS_EAGER", "False")
        environ["CELERY_TASK_ALWAYS_EAGER"] = "False"
        steps.add(
            [
                Command(
                    command="rabbitmq-server",
                    desc="Booting the rabbitMQ server with default config",
                    log_file="run_rabbitmq",
                    verbose=verbose,
                ),
                Command(
                    command="pm2 start ./legl_dev/pm2.config.js",
                    desc="Spinning up process manager for celery queue consumers",
                    log_file="run_pm2",
                    verbose=verbose,
                ),
                Command(
                    command="pm2 log",
                    desc="Starting pm2 logger",
                    log_file="pm2_logger",
                    verbose=verbose,
                ),
                Command(
                    command="rabbitmq-diagnostics log_tail_stream",
                    desc="Starting rabbitmq logger",
                    log_file="rabbitmq_logger",
                    verbose=verbose,
                ),
            ]
        )
    else:
        environ.pop("CELERY_TASK_ALWAYS_EAGER", None)

    if webpack:
        steps.add(
            Command(
                command=f"{docker_command(mutagen)} up frontend",
                desc="Starting webpack",
                log_file="start_webpack",
                verbose=verbose,
            )
        )

    steps.run()


@app.command(help="Rebuild the local enviroment")
def build(
    verbose: bool = typer.Option(False, help="Run the command in verbose mode"),
    mutagen: bool = typer.Option(False, help="Run docker with Mutagen"),
    cache: bool = typer.Option(True, help="Drop the database and create a fresh one"),
) -> None:

    extra_args = f"{'' if cache else '--no-cache'} "
    steps = Steps(
        steps=[
            Command(
                log_file="building_docker_image",
                desc="Building docker image",
                command=f"{docker_command(mutagen)} build {extra_args}",
                verbose=verbose,
            ),
        ],
    )
    steps.add(
        [
            Command(
                log_file="run_migrations",
                desc="Running migrations",
                command=f"{docker_command(mutagen)} exec backend python manage.py migrate",
                verbose=verbose,
            ),
            Command(
                log_file="flush",
                desc="Flushing database data",
                command=f"{docker_command(mutagen)} exec backend python manage.py flush --noinput",
                verbose=verbose,
            ),
            Command(
                log_file="create_factories",
                desc="Creating factory data",
                command=f"{docker_command(mutagen)} exec backend python manage.py run_factories",
                verbose=verbose,
            ),
            Command(
                log_file="create_emails",
                desc="Seeding emails",
                command=f"{docker_command(mutagen)} exec backend python manage.py seed_emails",
                verbose=verbose,
            ),
        ]
    )
    steps.run()

    print("Build complete 🚀")


@app.command(help="Run the local pytest unit tests")
def pytest(
    verbose: bool = typer.Option(True, help="Run the command in verbose mode",),
    mutagen: bool = typer.Option(False, help="Run docker with Mutagen"),
    full_diff: bool = typer.Option(False, help="Show full diff in errors",),
    create_db: bool = typer.Option(False, help="Recreates the test database",),
    last_failed: bool = typer.Option(False, help="Run the last failed tests",),
    warnings: bool = typer.Option(False, help="Toggle warnings in output",),
    gui: bool = typer.Option(True, help="Toggle the output gui",),
    snapshot_update: bool = typer.Option(False, help="update snapshots",),
    show_capture: bool = typer.Option(False, help="show captured stdout",),
    parallel: bool = typer.Option(False, help="run tests in parallel",),
    all_logs: bool = typer.Option(
        False, help="show print outputs instead of just logs",
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
                log_file="run_unit_tests",
                desc="Running unit tests",
                command=f"{docker_command(mutagen)} exec backend pytest --html=unit_test_results.html {extra_args} {path}",
                verbose=verbose,
            ),
        ]
    )
    if gui:
        steps.add(
            Command(
                log_file="open_unit_test_results",
                desc="Opening test results",
                command=f"open ./unit_test_results.html",
                verbose=verbose,
            )
        )

    if snapshot_update:
        steps.add(
            Command(
                log_file="black",
                desc="Blacking codebase",
                command=f"{docker_command(mutagen)} exec backend black .",
                verbose=verbose,
            )
        )
    steps.run()


@app.command(help="Format the code with isort, black and prettier")
def format(
    verbose: bool = typer.Option(False, help="Run the command in verbose mode"),
    mutagen: bool = typer.Option(False, help="Run docker with Mutagen"),
    push: bool = typer.Option(False, help="Also push the changes to the repo"),
):

    steps = Steps(
        steps=[
            Command(
                log_file="isort",
                desc="sorting python imports",
                command=f"{docker_command(mutagen)} exec backend isort .",
                verbose=verbose,
            ),
            Command(
                log_file="black",
                desc="blacking codebase",
                command=f"{docker_command(mutagen)} exec backend black .",
                verbose=verbose,
            ),
            Command(
                log_file="pretty",
                desc="prettifiying codebase",
                command=f"{docker_command(mutagen)} exec frontend yarn run format:prettier",
                verbose=verbose,
            ),
        ]
    )
    if push:
        steps.add(
            [
                Command(
                    log_file="git_stage",
                    desc="staging changes",
                    command="git stage .",
                    verbose=verbose,
                ),
                Command(
                    log_file="git_commit",
                    desc="commiting changes",
                    command='git commit -m "formatting"',
                    verbose=verbose,
                ),
                Command(
                    log_file="git_push", desc="pushing changes", command="git push"
                ),
            ]
        )
    steps.run()


@app.command(help="Open Cypress e2e tests")
def cypress(
        verbose: bool = typer.Option(True, help="Run the command in verbose mode"),
        mutagen: bool = typer.Option(False, help="Run docker with Mutagen")
    ):

    steps = Steps(
        steps=[
            Command(
                log_file="cypress",
                desc="running cypress",
                command=f"{docker_command(mutagen)} exec frontend yarn run cypress open",
                verbose=verbose,
            )
        ]
    )
    steps.run()


@app.command(help="Create and run migrations")
def migrate(
    verbose: bool = typer.Option(False, help="Run the command in verbose mode"),
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
                log_file="merge_migrations",
                desc="Merging migration",
                command=f"{docker_command(mutagen)} exec backend python manage.py makemigrations --merge",
                verbose=True,
            ),
        )
    if make:
        steps.add(
            Command(
                log_file="make_migrations",
                desc="Making migrations",
                command=f"{docker_command(mutagen)} exec backend python manage.py makemigrations",
                verbose=verbose,
            ),
        )
    if run:
        steps.add(
            Command(
                log_file="run_migrations",
                desc="Running migrations",
                command=f"{docker_command(mutagen)} exec backend python manage.py migrate",
                verbose=verbose,
            ),
        )
    steps.add(
        Command(
            log_file="black",
            desc="blacking codebase",
            command=f"{docker_command(mutagen)} exec backend black .",
            verbose=verbose,
        ),
    )
    steps.run()


@app.command(help="Clean out and create new factories")
def factories(
    verbose: bool = typer.Option(False, help="Run the command in verbose mode"),
    mutagen: bool = typer.Option(False, help="Run docker with Mutagen"),
    emails: bool = typer.Option(True, help="Generate factory emails"),
):

    steps = Steps(
        steps=[
            Command(
                log_file="flush",
                desc="Flushing",
                command=f"{docker_command(mutagen)} exec backend python manage.py flush --noinput",
                verbose=verbose,
            ),
            Command(
                log_file="create_factories",
                desc="Creating factory data",
                command=f"{docker_command(mutagen)} exec backend python manage.py run_factories",
                verbose=verbose,
            ),
        ],
    )
    if emails:
        steps.add(
            Command(
                log_file="create_emails",
                desc="Seeding emails",
                command=f"{docker_command(mutagen)} exec backend python manage.py seed_emails",
                verbose=verbose,
            ),
        )
    steps.run()


@app.command(help="Cleans out git branches")
def gitclean(
    verbose: bool = typer.Option(False, help="Run the command in verbose mode"),
):
    steps = Steps(
        steps=[
            Command(
                log_file="gitclean",
                desc="Cleaning out git branches",
                command='git branch --merged | egrep -v "(^\\*|master|dev)" | xargs git branch -d',
                verbose=verbose,
                shell=True,
            ),
        ]
    )
    steps.run()


@app.command(help="Run JS unit tests")
def jstest(
    verbose: bool = typer.Option(True, help="Run the command in verbose mode"),
    mutagen: bool = typer.Option(False, help="Run docker with Mutagen"),
):

    steps = Steps(
        steps=[
            Command(
                log_file="jstest",
                desc="Running JS unit tests",
                command=f"{docker_command(mutagen)} exec frontend yarn run test",
                verbose=verbose,
            ),
            Command(
                log_file="js_code_cov",
                desc="Opening code coverage",
                command="open js-test-results/index.html",
                verbose=verbose,
            ),
        ]
    )
    steps.run()


if __name__ == "__main__":
    app()
