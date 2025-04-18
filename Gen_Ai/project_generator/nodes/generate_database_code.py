def generate_database_code_node(state):
    database_code = """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    """
    with open("output/app/database.py", "w") as f:
        f.write(database_code)
    return state