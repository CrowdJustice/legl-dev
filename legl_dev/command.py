#!/usr/bin/env python3
import typer
from subprocess import run, CalledProcessError
from typing import Union


class Command:
    def __init__(
        self,
        command: str,
        shell: bool = False,
    ) -> None:
        self.command = command
        self.shell = shell

    def run(self) -> None:
        try:
            run(
                self.command if self.shell else self.command.split(),
                universal_newlines=True,
                shell=self.shell,
                check=True,
            )
            typer.secho(f"✅  Command successful!", fg=typer.colors.GREEN)
        except CalledProcessError:
            typer.secho(f"⚠️  Command exited without a none 0 exit!", fg=typer.colors.YELLOW)


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
