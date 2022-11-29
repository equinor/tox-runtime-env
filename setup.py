from setuptools import setup


def local_scheme(version):
    return ""


setup(use_scm_version={
    "local_scheme": local_scheme,
    "write_to": "src/tox_runtime_env/version.py",
})
