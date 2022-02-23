from unittest import mock

from legl_dev.main import start


@mock.patch("legl_dev.command.run")
def test_standard_start(run):
    start(https=False, webpack=True)
    calls = [
        mock.call(
            ["docker", "compose", "stop"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
        mock.call(
            ["docker", "compose", "up", "backend", "-d"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
        mock.call(
            ["docker", "compose", "up", "frontend", "-d"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
        mock.call(
            ["docker", "compose", "logs", "-f"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
    ]
    run.assert_has_calls(calls)


@mock.patch("legl_dev.command.run")
def test_backend_only_start(run):
    start(https=False, webpack=False)
    calls = [
        mock.call(
            ["docker", "compose", "stop"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
        mock.call(
            ["docker", "compose", "up", "backend", "-d"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
        mock.call(
            ["docker", "compose", "logs", "-f"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
    ]
    run.assert_has_calls(calls)


@mock.patch("legl_dev.command.run")
def test_https_start(run):
    start(https=True, webpack=True)
    calls = [
        mock.call(
            ["docker", "compose", "stop"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
        mock.call(
            [
                "docker",
                "compose",
                "exec",
                "backend",
                "python",
                "manage.py",
                "runsslserver",
                "0.0.0.0:443",
                "-e",
                "HOST_SCHEME=https",
                "DEV_LOCAL_INSTALLED_APPS='[\"sslserver\"]'",
                "-d",
            ],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
        mock.call(
            ["docker", "compose", "up", "frontend", "-d"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
        mock.call(
            ["docker", "compose", "logs", "-f"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
    ]
    run.assert_has_calls(calls)
