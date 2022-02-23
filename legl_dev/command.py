#!/usr/bin/env python3

from subprocess import run
from threading import Thread
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
        run(
            self.command if self.shell else self.command.split(),
            universal_newlines=True,
            shell=self.shell,
            check=True,
        )


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
