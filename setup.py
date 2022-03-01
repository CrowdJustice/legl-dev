# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["legl_dev"]

package_data = {"": ["*"]}

install_requires = ["black==19.10b0", "isort==5.9.3", "typer>=0.4.0"]

entry_points = {"console_scripts": ["legl-dev = legl_dev.main:app"]}

setup_kwargs = {
    "name": "legl-dev",
    "version": "1.0.6",
    "description": "",
    "long_description": '# `legl-dev`\n\n**Usage**:\n\n```console\n$ legl-dev [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `build`: Rebuild the local enviroment\n* `cypress`: Open Cpyress e2e tests\n* `factories`: Clean out and create new factories\n* `format`: Format the code with black and prettier\n* `gitclean`: Cleans out git branches\n* `jstest`: Run JS unit tests\n* `migrate`: Create and run migrations\n* `pytest`: Run the local pytest unit tests\n* `start`: Start the dev enviroment\n* `update`: Update dependancies\n\n## `legl-dev build`\n\nRebuild the local enviroment\n\n**Usage**:\n\n```console\n$ legl-dev build [OPTIONS]\n```\n\n**Options**:\n\n* `--verbose / --no-verbose`: Run the command in verbose mode  [default: False]\n* `--create-db / --no-create-db`: Drop the database and create a fresh one  [default: False]\n* `--help`: Show this message and exit.\n\n## `legl-dev cypress`\n\nOpen Cpyress e2e tests\n\n**Usage**:\n\n```console\n$ legl-dev cypress [OPTIONS]\n```\n\n**Options**:\n\n* `--verbose / --no-verbose`: Run the command in verbose mode  [default: True]\n* `--help`: Show this message and exit.\n\n## `legl-dev factories`\n\nClean out and create new factories\n\n**Usage**:\n\n```console\n$ legl-dev factories [OPTIONS]\n```\n\n**Options**:\n\n* `--verbose / --no-verbose`: Run the command in verbose mode  [default: False]\n* `--help`: Show this message and exit.\n\n## `legl-dev format`\n\nFormat the code with black and prettier\n\n**Usage**:\n\n```console\n$ legl-dev format [OPTIONS]\n```\n\n**Options**:\n\n* `--verbose / --no-verbose`: Run the command in verbose mode  [default: False]\n* `--push / --no-push`: Also push the changes to the repo  [default: False]\n* `--help`: Show this message and exit.\n\n## `legl-dev gitclean`\n\nCleans out git branches\n\n**Usage**:\n\n```console\n$ legl-dev gitclean [OPTIONS]\n```\n\n**Options**:\n\n* `--verbose / --no-verbose`: Run the command in verbose mode  [default: False]\n* `--help`: Show this message and exit.\n\n## `legl-dev jstest`\n\nRun JS unit tests\n\n**Usage**:\n\n```console\n$ legl-dev jstest [OPTIONS]\n```\n\n**Options**:\n\n* `--verbose / --no-verbose`: Run the command in verbose mode  [default: True]\n* `--help`: Show this message and exit.\n\n## `legl-dev migrate`\n\nCreate and run migrations\n\n**Usage**:\n\n```console\n$ legl-dev migrate [OPTIONS]\n```\n\n**Options**:\n\n* `--verbose / --no-verbose`: Run the command in verbose mode  [default: False]\n* `--merge / --no-merge`: Run a migration merge first  [default: False]\n* `--help`: Show this message and exit.\n\n## `legl-dev pytest`\n\nRun the local pytest unit tests\n\n**Usage**:\n\n```console\n$ legl-dev pytest [OPTIONS] [PATH]\n```\n\n**Arguments**:\n\n* `[PATH]`: path for specific test in the format "<file path>::<class name>::<function name>"  [default: ]\n\n**Options**:\n\n* `--verbose / --no-verbose`: Run the command in verbose mode  [default: False]\n* `--full-diff / --no-full-diff`: Show full diff in errors  [default: False]\n* `--create-db / --no-create-db`: Recreates the test database  [default: False]\n* `--last-failed / --no-last-failed`: Run the last failed tests  [default: False]\n* `--warnings / --no-warnings`: Toggle warnings in output  [default: True]\n* `--gui / --no-gui`: Toggle the output gui  [default: True]\n* `--help`: Show this message and exit.\n\n## `legl-dev start`\n\nStart the dev enviroment\n\n**Usage**:\n\n```console\n$ legl-dev start [OPTIONS]\n```\n\n**Options**:\n\n* `--verbose / --no-verbose`: Run the command in verbose mode  [default: True]\n* `--help`: Show this message and exit.\n\n## `legl-dev update`\n\nUpdate dependancies\n\n**Usage**:\n\n```console\n$ legl-dev update [OPTIONS]\n```\n\n**Options**:\n\n* `--verbose / --no-verbose`: Run the command in verbose mode  [default: False]\n* `--help`: Show this message and exit.\n',
    "author": "phil-bell",
    "author_email": "philhabell@gmail.com",
    "maintainer": None,
    "maintainer_email": None,
    "url": None,
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.7,<4.0",
}


setup(**setup_kwargs)
