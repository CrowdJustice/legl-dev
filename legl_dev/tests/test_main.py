from unittest import mock

from legl_dev.main import start


@mock.patch("legl_dev.command.run")
def test_standard_start(run):
    start()
    calls = [
        mock.call(
            ["docker", "compose", "up"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
    ]
    run.assert_has_calls(calls)
