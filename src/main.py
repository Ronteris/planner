from typing import List

from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine
from item import router as item_router
from models import User
from schemas import CreateUser, ReadUser

app = FastAPI()

app.include_router(item_router, prefix='/item', tags=['items'])


@app.get('/')
async def hello():
    return {'hello': 'world'}


@app.post('/user')
async def add_user(user: CreateUser) -> dict:
    async with AsyncSession(engine) as session:
        stmt = User(name=user.name, fullname=user.fullname,
                    nickname=user.nickname)
        session.add(stmt)
        await session.commit()
        return {'status': 'OK'}


@app.get('/user')
async def user_list() -> List[ReadUser]:
    async with AsyncSession(engine) as session:
        stmt = select(User)
        result = await session.scalars(stmt)
        users = result.all()
    return users


@app.get('/user/{user_id}')
async def get_user(user_id:int) -> ReadUser:
    async with AsyncSession(engine) as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.scalars(stmt)
    return result.first()

@app.put()
async def update_user():pass