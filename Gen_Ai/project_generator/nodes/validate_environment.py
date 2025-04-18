def validate_environment_node(state):
    import shutil, sys
    assert shutil.which("psql"), "PostgreSQL CLI not installed."
    assert sys.version_info >= (3, 8), "Python 3.8+ is required."
    return state