#!/usr/bin/env python3
import pathlib
import subprocess
from typing import Union

import typer


class Command:
    def __init__(
        self,
        command: str,
        shell: bool = False,
    ) -> None:
        self.command = command
        self.shell = shell

    def _success_output(self):
        typer.secho(f"✅  Command successful!", fg=typer.colors.GREEN)

    def _error_output(self, e):
        typer.secho(
            f"⚠️  Command exited with code {e.returncode}! Check the logs: logs/legl-dev.logs",
            fg=typer.colors.YELLOW,
        )

    def _command_output(self):
        typer.secho(f"Running: {self.command}", fg=typer.colors.MAGENTA)

    def write_logs(self, result):
        pathlib.Path("logs").mkdir(parents=True, exist_ok=True)
        with open("logs/legl-dev.logs", "a") as logs:
            logs.write("\n===================== new command =====================\n")
            logs.write(f"Command run: {self.command}\n")
            logs.write(f"Logs:\n\n {result.stdout}\n{result.stderr}")

    def run(self) -> None:
        self._command_output()
        try:
            result = subprocess.run(
                self.command if self.shell else self.command.split(),
                universal_newlines=True,
                shell=self.shell,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.write_logs(result)
            self._success_output()
        except subprocess.CalledProcessError as e:
            self._error_output(e)

    def run_verbose(self):
        self._command_output()
        try:
            subprocess.run(
                self.command if self.shell else self.command.split(),
                universal_newlines=True,
                shell=self.shell,
                check=True,
            )
            self._success_output()
        except subprocess.CalledProcessError as e:
            self._error_output(e)


class Steps:
    def __init__(self, steps: list = None) -> None:
        self.steps = steps or []

    def add(self, steps: Union[list, Command]) -> None:
        try:
            self.steps += steps
        except TypeError:
            self.steps += [steps]

    def run(self) -> None:
        for step in self.steps:
            step.run()
