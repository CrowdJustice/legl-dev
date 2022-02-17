import io
from unittest import mock

from legl_dev.command import Command, Steps


@mock.patch("legl_dev.command.run")
def test_run_in_verbose_mode(run):
    command = Command(log_file="test", desc="test", command="echo test", verbose=True)
    command.run()
    run.assert_called_with(["echo", "test"], universal_newlines=True, shell=False)


@mock.patch("legl_dev.command.yaspin")
def test_run_not_in_verbose_mode(yaspin):
    command = Command(log_file="test", desc="test", command="echo test", verbose=False)
    command.run()
    yaspin.assert_called_with(text="test", color="yellow")
