def finalize_project_node(state):
    with open("output/app/main.py", "w") as f:
        f.write("""
from fastapi import FastAPI
from app.api.routes import user, item
app = FastAPI()
app.include_router(user.router)
app.include_router(item.router)
        """)
    with open("output/Dockerfile", "w") as f:
        f.write("""
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
        """)
    with open("output/requirements.txt", "w") as f:
        f.write("fastapi\nuvicorn\nsqlalchemy\npsycopg2-binary\nalembic\n")
    with open("output/.env", "w") as f:
        f.write("DATABASE_URL=postgresql://user:password@localhost/dbname\n")
    with open("output/README.md", "w") as f:
        f.write("# FastAPI Project generated from SRS\n")
    return state