from unittest import mock

from legl_dev import main


@mock.patch("legl_dev.command.run")
def test_standard_start(run):
    main.start()
    calls = [
        mock.call(
            ["docker", "compose", "up"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
    ]
    run.assert_has_calls(calls)


@mock.patch("legl_dev.command.run")
def test_install_pip(run):
    main.install(
        package="example",
        pip=True,
        yarn=False,
        self=False,
        version="main",
        upgrade=False,
    )
    calls = [
        mock.call(
            ["docker", "exec", "backend", "pip", "install", "example"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
        mock.call(
            "docker exec backend pip freeze | grep example >> requirements.txt",
            universal_newlines=True,
            shell=True,
            check=True,
        ),
    ]
    run.assert_has_calls(calls)


@mock.patch("legl_dev.command.run")
def test_install_pip_upgrade(run):
    main.install(
        package="example",
        pip=True,
        yarn=False,
        self=False,
        version="main",
        upgrade=True,
    )
    calls = [
        mock.call(
            ["docker", "exec", "backend", "pip", "install", "--upgrade", "example"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
        mock.call(
            "docker exec backend pip freeze | grep example >> requirements.txt",
            universal_newlines=True,
            shell=True,
            check=True,
        ),
    ]
    run.assert_has_calls(calls)


@mock.patch("legl_dev.command.run")
def test_install_yarn(run):
    main.install(
        package="example",
        pip=False,
        yarn=True,
        self=False,
        version="main",
        upgrade=False,
    )
    calls = [
        mock.call(
            ["docker", "exec", "frontend", "yarn", "add", "example"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
    ]
    run.assert_has_calls(calls)


@mock.patch("legl_dev.command.run")
def test_install_yarn_upgrade(run):
    main.install(
        package="example",
        pip=False,
        yarn=True,
        self=False,
        version="main",
        upgrade=True,
    )
    calls = [
        mock.call(
            ["docker", "exec", "frontend", "yarn", "up", "example"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
    ]
    run.assert_has_calls(calls)


@mock.patch("legl_dev.command.run")
def test_install_self(run):
    main.install(
        package="example",
        pip=False,
        yarn=False,
        self=True,
        version="main",
        upgrade=False,
    )
    calls = [
        mock.call(
            ["pip", "uninstall", "legl-dev", "-y"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
        mock.call(
            ["pip", "install", "git+https://github.com/CrowdJustice/legl-dev.git@main"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
    ]
    run.assert_has_calls(calls)


@mock.patch("legl_dev.command.run")
def test_install_self_upgrade(run):
    main.install(
        package="example",
        pip=False,
        yarn=False,
        self=True,
        version="main",
        upgrade=True,
    )
    calls = [
        mock.call(
            ["pip", "install", "--upgrade", "legl-dev"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
    ]
    run.assert_has_calls(calls)


@mock.patch("legl_dev.command.run")
def test_remote_no_commands(run):
    main.remote()
    calls = [
        mock.call(
            ["docker", "compose", "exe", "backend", "bash"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
    ]
    run.assert_has_calls(calls)

@mock.patch("legl_dev.command.run")
def test_remote_frontend_commands(run):
    main.remote("frontend")
    calls = [
        mock.call(
            ["docker", "compose", "exe", "frontend", "bash"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
    ]
    run.assert_has_calls(calls)

@mock.patch("legl_dev.command.run")
def test_remote_frontend_commands(run):
    main.remote("frontend")
    calls = [
        mock.call(
            ["docker", "compose", "exe", "frontend", "bash"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
    ]
    run.assert_has_calls(calls)
