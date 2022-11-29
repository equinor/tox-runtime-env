[![Latest version on
PyPi](https://badge.fury.io/py/tox-runtime-env.svg)](https://badge.fury.io/py/tox-runtime-env)
[![Supported Python
versions](https://img.shields.io/pypi/pyversions/tox-runtime-env.svg)](https://pypi.org/project/tox-runtime-env/)
[![Azure Pipelines build
status](https://dev.azure.com/equinor/tox-runtime-env/_apis/build/status/tox%20ci?branchName=main)](https://dev.azure.com/equinor/tox-runtime-env/_build/latest?definitionId=9&branchName=main)
[![Documentation
status](https://readthedocs.org/projects/tox-runtime-env/badge/?version=latest&style=flat-square)](https://tox-runtime-env.readthedocs.io/en/latest/?badge=latest)
[![Code style:
black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

# tox-runtime-env

A tox plugin to determine and set environment variables at runtime.

Features
--------

* Set environment variables for tox test environments at runtime, during
    configuration setup
* The values of these variables can be gathered from dynamic system data via shell commands
* Multiple shell commands can be formatted into a given variable value
* This (may) free you from manually setting environment variables required
    by tests or by what you're testing if certain environment variables
    change over time, e.g. `PYTHONPATH`, `LD_LIBRARY_PATH`, etc in a software distribution
* Variables set in this manner can be used in tandem with tox's standard
    `setenv`


Requirements
------------

* tox
* Python >= 3.8


Installation
------------

You can install "tox-runtime-env" via [pip](https://pypi.org/project/pip/) from [PyPI](https://pypi.org):

```
pip install tox-runtime-env
```

Usage
-----

In a tox testenv, define a `runtime_env` section. This section must contain a list of environment
variable names and values defined in the same way that tox's default `setenv` environment variables
are. The only difference is that is can do more: it can format the output of shell commands within
variable values.

Here is a simple example:
```ini
[testenv]
runtime_env =
    SOME_VAR = good$(echo bye)
    OTHER_VAR = $(echo Hello) $(echo world)
```
This will set
```python
os.environ["SOME_VAR"] = "goodbye"
os.environ["OTHER_VAR"] = "Hello world"
```
in the tox runtime context. Statements within `$()` are executed by the shell. These commands can
be invoked (and piped) as if typed into a command line. This allows you as well to access these
environment variables in a `setenv` section, so you can do something like the following:

```ini
[testenv]
runtime_env =
    _ROOT_PATH = /root/path/somewhere
    _TEST_VERSION = $(grep "someval" /some/testing/file | cut -d "," -f 2)
    _STABLE_VERSION = $(grep "someval" /some/stable/file | cut -d "," -f 2)
    _RHEL7_VERSION = $(grep "rhel7" /some/rhel7/file | cut -d "," -f 2)-rhel7
setenv =
    PYTHONPATH = {env:_ROOT_PATH}/{env:_STABLE_VERSION}

[testenv:rhel]
setenv =
    PYTHONPATH = {env:_ROOT_PATH}/{env:_RHEL7_VERSION}
    LD_LIBRARY_PATH = {env:_ROOT_PATH}/lib/{env:_RHEL7_VERSION}
```

Contributing
------------
Contributions are welcome. Tests can be run with [tox](https://tox.readthedocs.io/en/latest/), please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the **MIT** license, `tox-runtime-env` is
free and open source software.


Issues
------

* Parsing shell commands is quite naive and will misbehave if your shell command contains a `)`
    that is not meant to terminate the command, e.g. `$(grep something | cut -d ")" -f 2)`

If you encounter any problems, please
[file an issue](https://github.com/equinor/tox-runtime-env/issues)
along with a detailed description.
