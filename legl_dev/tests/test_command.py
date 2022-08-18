from unittest import mock

from legl_dev.command import Command, Steps


@mock.patch("legl_dev.command.subprocess.run")
def test_command_run(run):
    command = Command(command="echo test")
    command.run()
    run.assert_called_with(
        ["echo", "test"], universal_newlines=True, shell=False, check=True
    )


@mock.patch("legl_dev.command.subprocess.run")
def test_command_run_with_shell(run):
    command = Command(command="echo test", shell=True)
    command.run()
    run.assert_called_with("echo test", universal_newlines=True, shell=True, check=True)


def test_adding_commands_to_steps():
    test_command_one = Command(command="echo test one")
    test_command_two = Command(command="echo test two")
    steps = Steps([test_command_one])
    steps.add(test_command_two)
    assert steps.steps == [test_command_one, test_command_two]


def test_adding_commands_to_empty_steps():
    test_command_one = Command(command="echo test one")
    test_command_two = Command(command="echo test two")
    steps = Steps()
    steps.add(test_command_one)
    steps.add(test_command_two)
    assert steps.steps == [test_command_one, test_command_two]


def test_adding_list_of_commands_to_steps():
    test_command_one = Command(command="echo test one")
    test_command_two = Command(command="echo test two")
    test_command_three = Command(command="echo test three")
    steps = Steps([test_command_one])
    steps.add([test_command_two, test_command_three])
    assert steps.steps == [test_command_one, test_command_two, test_command_three]


def test_steps_dont_overflow_instance():
    test_command_one = Command(command="echo test one")
    test_command_two = Command(command="echo test two")
    steps_one = Steps()
    steps_one.add(test_command_one)
    steps_two = Steps()
    steps_two.add(test_command_two)
    assert steps_one.steps == [test_command_one]
    assert steps_two.steps == [test_command_two]


@mock.patch("legl_dev.command.subprocess.run")
def test_standard_start(run):
    test_command_one = Command(command="echo test one")
    test_command_two = Command(command="echo test two")
    steps = Steps([test_command_one])
    steps.add(test_command_two)
    steps.run()
    calls = [
        mock.call(
            ["echo", "test", "one"], universal_newlines=True, shell=False, check=True
        ),
        mock.call(
            ["echo", "test", "two"],
            universal_newlines=True,
            shell=False,
            check=True,
        ),
    ]
    run.assert_has_calls(calls)
