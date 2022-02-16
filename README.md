# `legl-dev`

**Usage**:

```console
$ legl-dev [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `build`: Rebuild the local enviroment
* `cypress`: Open Cpyress e2e tests
* `factories`: Clean out and create new factories
* `format`: Format the code with black and prettier
* `gitclean`: Cleans out git branches
* `jstest`: Run JS unit tests
* `migrate`: Create and run migrations
* `pytest`: Run the local pytest unit tests
* `start`: Start the dev enviroment
* `update`: Update dependancies

## `legl-dev build`

Rebuild the local enviroment

**Usage**:

```console
$ legl-dev build [OPTIONS]
```

**Options**:

* `--verbose / --no-verbose`: Run the command in verbose mode  [default: False]
* `--create-db / --no-create-db`: Drop the database and create a fresh one  [default: False]
* `--help`: Show this message and exit.

## `legl-dev cypress`

Open Cpyress e2e tests

**Usage**:

```console
$ legl-dev cypress [OPTIONS]
```

**Options**:

* `--verbose / --no-verbose`: Run the command in verbose mode  [default: True]
* `--help`: Show this message and exit.

## `legl-dev factories`

Clean out and create new factories

**Usage**:

```console
$ legl-dev factories [OPTIONS]
```

**Options**:

* `--verbose / --no-verbose`: Run the command in verbose mode  [default: False]
* `--help`: Show this message and exit.

## `legl-dev format`

Format the code with black and prettier

**Usage**:

```console
$ legl-dev format [OPTIONS]
```

**Options**:

* `--verbose / --no-verbose`: Run the command in verbose mode  [default: False]
* `--push / --no-push`: Also push the changes to the repo  [default: False]
* `--help`: Show this message and exit.

## `legl-dev gitclean`

Cleans out git branches

**Usage**:

```console
$ legl-dev gitclean [OPTIONS]
```

**Options**:

* `--verbose / --no-verbose`: Run the command in verbose mode  [default: False]
* `--help`: Show this message and exit.

## `legl-dev jstest`

Run JS unit tests

**Usage**:

```console
$ legl-dev jstest [OPTIONS]
```

**Options**:

* `--verbose / --no-verbose`: Run the command in verbose mode  [default: True]
* `--help`: Show this message and exit.

## `legl-dev migrate`

Create and run migrations

**Usage**:

```console
$ legl-dev migrate [OPTIONS]
```

**Options**:

* `--verbose / --no-verbose`: Run the command in verbose mode  [default: False]
* `--merge / --no-merge`: Run a migration merge first  [default: False]
* `--help`: Show this message and exit.

## `legl-dev pytest`

Run the local pytest unit tests

**Usage**:

```console
$ legl-dev pytest [OPTIONS] [PATH]
```

**Arguments**:

* `[PATH]`: path for specific test in the format "<file path>::<class name>::<function name>"  [default: ]

**Options**:

* `--verbose / --no-verbose`: Run the command in verbose mode  [default: False]
* `--full-diff / --no-full-diff`: Show full diff in errors  [default: False]
* `--create-db / --no-create-db`: Recreates the test database  [default: False]
* `--last-failed / --no-last-failed`: Run the last failed tests  [default: False]
* `--warnings / --no-warnings`: Toggle warnings in output  [default: True]
* `--gui / --no-gui`: Toggle the output gui  [default: True]
* `--help`: Show this message and exit.

## `legl-dev start`

Start the dev enviroment

**Usage**:

```console
$ legl-dev start [OPTIONS]
```

**Options**:

* `--verbose / --no-verbose`: Run the command in verbose mode  [default: True]
* `--help`: Show this message and exit.

## `legl-dev update`

Update dependancies

**Usage**:

```console
$ legl-dev update [OPTIONS]
```

**Options**:

* `--verbose / --no-verbose`: Run the command in verbose mode  [default: False]
* `--help`: Show this message and exit.
