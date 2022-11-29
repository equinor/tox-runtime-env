import os
from unittest import mock


@mock.patch.dict("os.environ")
def test_config_run_empty(initproj, cmd):
    initproj(
        "pkg123-0.7",
        filedefs={
            "tox.ini": """
                [tox]
                envlist = py, b
                skipsdist = True
                [testenv]
                runtime_env = _TEST_RUN_ENV =
                commands=python -c "print('perform')"
                [testenv:b]
                cinderella = True
            """
        },
    )
    result = cmd()
    result.assert_fail(is_run_test_env=False)


@mock.patch.dict("os.environ")
def test_config_run_simple(initproj, cmd):
    initproj(
        "pkg123-0.7",
        filedefs={
            "tox.ini": """
                [tox]
                envlist = py, b
                skipsdist = True
                [testenv]
                runtime_env =
                    _TEST_RUN_ENV = True
                    #_TEST_RUN_IGNORE = False
                commands=python -c "print('perform')"
                [testenv:b]
                cinderella = True
            """
        },
    )
    result = cmd()
    result.assert_success(is_run_test_env=False)
    assert os.getenv("_TEST_RUN_ENV") == "True"
    assert os.getenv("_TEST_RUN_IGNORE") is None


@mock.patch.dict("os.environ")
def test_config_run_shell(initproj, cmd):
    initproj(
        "pkg123-0.7",
        filedefs={
            "tox.ini": """
                [tox]
                envlist = py, b
                skipsdist = True
                [testenv]
                runtime_env =
                    _TEST_RUN_ENV = $(echo True)
                    ; _TEST_RUN_IGNORE = False
                commands=python -c "print('perform')"
                [testenv:b]
                cinderella = True
            """
        },
    )
    result = cmd()
    result.assert_success(is_run_test_env=False)
    assert os.getenv("_TEST_RUN_ENV") == "True"
    assert os.getenv("_TEST_RUN_IGNORE") is None
