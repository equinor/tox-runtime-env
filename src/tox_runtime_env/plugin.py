import os
import subprocess

import pluggy

hookimpl = pluggy.HookimplMarker("tox")


class ToxRuntimeEnvError(Exception):
    pass


def _has_shell_command(value):
    """Checks if environment value is meant to be determined from the
    execution of shell commands."""
    start = value.find("$(")
    end = value.find(")")
    if start == -1 or end == -1:
        return False
    return start < end


def _parse_env_value(value):
    """Parses the string used to construct the environment variable value,
    which may be just a sequence of shell commands, or a formatted string
    of shell commands and text interleaved"""
    if not _has_shell_command(value):
        return value

    start = value.index("$(")
    end = value.index(")")
    if start != 0:
        return value[:start] + _parse_env_value(value[start:])

    return _exec_shell_cmd(value[2:end]) + _parse_env_value(value[end + 1 :])  # noqa


def _exec_shell_cmd(cmd):
    result = subprocess.run(
        ["sh", "-c", cmd],
        capture_output=True,
        check=True,
        text=True,
    )
    value = result.stdout.strip()
    return value


@hookimpl
def tox_configure(config):
    """Set environment variables during configuration"""
    for env in config.envlist:
        for entry in config.envconfigs[env]._reader.getlist("runtime_env"):
            key, value = entry.split("=", 1)
            key, value = key.strip(), value.strip()
            if not key or not value:
                raise ToxRuntimeEnvError("empty environment variable or value")

            if key.startswith("#") or key.startswith(";"):
                continue  # pragma: no cover

            if _has_shell_command(value):
                value = _parse_env_value(value)

            os.environ[key] = value
