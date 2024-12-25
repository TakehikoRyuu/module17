from fastapi import APIRouter, Body

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models.task import Task
from app.models.user import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify


router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.query(User).all()
    return users


@router.get("/user_id")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    try:
        user = db.scalar(select(User).filter_by(user_id=user_id))
        return user
    except HTTPException:
        raise HTTPException(status_code=404, detail="User was not found")


@router.post("/create")
async def create_user(create_user: Annotated[CreateUser, Body()], db: Annotated[Session, Depends(get_db)]):
    try:
        db.execute(insert(User).values(username=create_user.username,
                                       firstname=create_user.firstname,
                                       lastname=create_user.lastname,
                                       age=create_user.age))
        db.commit()
        return {'status_code': status.HTTP_201_CREATED,
                'transaction': 'Successful'}
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is register")


@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], update_user: UpdateUser, user_id: int):
    user = db.scalar(select(User).filter(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    db.execute(update(User).filter(User.id == user_id)).values(
        firstname=update_user.firstname,
        lastname=update_user.lastname,
        age=update_user.age)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).filter(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    db.execute(delete(User).where(User.id == user_id))
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'User update is successful!'}