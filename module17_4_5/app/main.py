# alembic revision --autogenerate -m "initial migration"
# alembic upgrade head
# uvicorn app.main:app --reload
from fastapi import FastAPI
from app.routers import task, user

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to Taskmanager"}



app.include_router(task.router)
app.include_router(user.router)






