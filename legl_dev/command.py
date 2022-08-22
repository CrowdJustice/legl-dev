#!/usr/bin/env python3
import pathlib
import shutil
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

    def _line_message(self, message):
        width, _ = shutil.get_terminal_size()
        line = "".join(["-" for _ in range((width - len(message) - 4) // 2)])
        return f"{line} {message} {line}"

    def _success_output(self):
        typer.secho(
            self._line_message(" ✅  Command successful! ✅ "),
            fg=typer.colors.GREEN,
        )

    def _error_output(self, e):
        typer.secho(
            f"💥 Command exited with code {e.returncode}! Check the logs above for more informations. 💥",
            fg=typer.colors.BRIGHT_RED,
        )

    def _command_output(self):
        typer.secho(
            self._line_message(f"🚧 Running: {self.command} 🚧"),
            fg=typer.colors.YELLOW,
        )

    def run(self):
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

    def run(self, verbose=False) -> None:
        for step in self.steps:
            step.run()
