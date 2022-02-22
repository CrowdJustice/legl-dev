import io
from unittest import mock

from legl_dev.command import Command, Steps


@mock.patch("legl_dev.command.run")
def test_run_in_verbose_mode(run):
    command = Command(log_file="test", desc="test", command="echo test", verbose=True)
    command.run()
    run.assert_called_with(["echo", "test"], universal_newlines=True, shell=False)


