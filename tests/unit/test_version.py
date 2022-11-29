def test_version():
    pkg = __import__("tox_runtime_env", fromlist=["__version__"])
    assert pkg.__version__
