import pytest

from tox_runtime_env.plugin import _exec_shell_cmd, _has_shell_command, _parse_env_value


def test_has_shell_command():
    assert _has_shell_command("") is False
    assert _has_shell_command("$()") is True
    assert _has_shell_command("hello") is False
    assert _has_shell_command("$(echo hello)") is True
    assert _has_shell_command("$(echo hello") is False
    assert _has_shell_command("echo hello)") is False
    assert _has_shell_command("hello$(echo hello)") is True
    assert _has_shell_command("$(echo hello)ab") is True
    assert _has_shell_command("ab$(echo hello)ab") is True
    assert _has_shell_command("ab$(echo hello)ab$(echo bye)") is True
    assert _has_shell_command("ab$(echo hello)ab$(echo bye") is True
    assert _has_shell_command("ab$(echo hello)ab$(echo bye)nn") is True
    assert _has_shell_command("ab$(echo helloab$(echo bye)nn") is True


def test_parse_env_value():
    assert _parse_env_value("hello") == "hello"
    assert _parse_env_value("$(echo hello)") == "hello"
    assert _parse_env_value("$(echo good)-bye") == "good-bye"
    assert _parse_env_value("$(echo good)-$(echo 'bye')") == "good-bye"
    assert _parse_env_value("he$(printf 'hello' | cut -b 3,4)o") == "hello"
    assert _parse_env_value("hel$(true)lo") == "hello"

    with pytest.raises(Exception):
        assert _parse_env_value("$(commandthatdoesntexist)")


def test_exec_shell_cmd():
    assert _exec_shell_cmd("echo hello") == "hello"
    assert _exec_shell_cmd("true") == ""
    assert _exec_shell_cmd("printf 'hello' | cut -b 3,4") == "ll"

    with pytest.raises(Exception):
        assert _exec_shell_cmd("commandthatdoesntexist")


def test_tox_configure(newconfig):
    pass
