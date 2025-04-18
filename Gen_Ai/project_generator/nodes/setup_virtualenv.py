def setup_virtualenv_node(state):
    import subprocess
    subprocess.run(["python3", "-m", "venv", "venv"], check=True)
    subprocess.run(["venv/bin/pip", "install", "fastapi", "uvicorn", "sqlalchemy", "psycopg2-binary", "alembic"], check=True)
    return state