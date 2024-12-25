from fastapi import APIRouter, Body

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models.task import Task
from app.models.user import User
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify


router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    task = db.query(Task).all()
    return task


@router.get("/task_id")
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    try:
        task = db.scalar(select(Task).filter_by(task_id=task_id))
        return task
    except HTTPException:
        raise HTTPException(status_code=404, detail="User was not found")


@router.get("/user_id/tasks")
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).filter(User.id == user_id))
    try:
        if user != None:
            task = db.query(select(Task).filter_by(user_id=user_id))
            return task
    except HTTPException:
        raise HTTPException(status_code=404, detail="User was not found")


@router.post("/create")
async def create_task(user_id: int, create_task: Annotated[CreateTask, Body()],
                      db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).filter(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=400, detail="User was not found")
    db.execute(insert(Task).values(title=create_task.title,
                                   content=create_task.content,
                                   priority=create_task.priority,
                                   user_id=user_id))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], update_task: UpdateTask, task_id: int):
    task = db.scalar(select(Task).filter(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=404, detail="User was not found")
    db.execute(update(Task).filter(Task.id == task_id)).values(
        title=update_task.title,
        content=update_task.content,
        priority=update_task.priority,
        user_id=update_task.task_id)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).filter(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=404, detail="User was not found")
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Task update is successful!'}


