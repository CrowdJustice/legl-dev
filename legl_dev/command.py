from datetime import datetime
from os import mkdir
from subprocess import CalledProcessError, run
from threading import Thread
from typing import Union

from yaspin import yaspin


class Command:
    def __init__(
        self, command: str, desc: str, log_file: str, verbose: bool = False, shell: bool = False,
    ) -> None:
        self.command = command
        self.desc = desc
        self.log_file = log_file
        self.verbose = verbose
        self.shell = shell

    def run(self) -> None:
        if self.verbose:
            run(
                self.command if self.shell else self.command.split(),
                universal_newlines=True,
                shell=self.shell,
            )
            return
        with yaspin(text=f"{self.desc}", color="yellow") as spinner:
            try:
                try:
                    mkdir("logs/")
                except FileExistsError:
                    pass
                with open(f"logs/{self.log_file}.log", "w") as outfile:
                    start_time = datetime.now()
                    run(
                        self.command if self.shell else self.command.split(),
                        stdout=outfile,
                        stderr=outfile,
                        shell=self.shell,
                    )
                    run_time = datetime.now() - start_time
                with open(f"logs/{self.log_file}.log", "r") as outfile:
                    if "error:" in outfile.read().lower():
                        spinner.text = f"{self.desc} - \033[93mWarning\033[0m please check: \33[34mlogs/{self.log_file}.log\033[4m"
                        spinner.fail("⚠")
                    else:
                        spinner.text = f"{self.desc} {' ' * (45-len(self.desc))}\033[93m[{str(run_time)[:-5]}]\033[0m"
                        spinner.color = "green"
                        spinner.ok("✔")
            except CalledProcessError:
                spinner.color = "red"
                spinner.fail("✖")


class Steps:
    def __init__(self, steps: list = [], concurrent: bool = False) -> None:
        self.steps = steps
        self.concurrent = concurrent

    def add(self, steps: Union[list, Command]) -> None:
        try:
            self.steps += steps
        except TypeError:
            self.steps += [steps]

    def run(self) -> None:
        for step in self.steps:
            if self.concurrent:
                Thread(target=step.run).start()
            else:
                step.run()
