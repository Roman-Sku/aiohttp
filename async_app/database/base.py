from typing import Self, Sequence
from unittest import result

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import declarative_base

from .connector import db_conn

Base = declarative_base()


class Manager:

    @classmethod
    async def create(cls, **kwargs) -> Self:
        obj = cls(**kwargs)
        async with db_conn.session as session:
            session.add(obj)            # Добавляем объект в его таблицу.
            await session.commit()      # Подтверждаем.
            await session.refresh(obj)  # Обновляем атрибуты у объекта, чтобы получить его primary key.
        return obj

    @classmethod
    async def get(cls, _id: int) -> Self:
        async with db_conn.session as session:
            result = await session.execute(
                select(cls).where(cls.id == _id)
            )
            return result.scalar_one()

    @classmethod
    async def all(cls) -> Sequence[Self]:
        async with db_conn.session as session:
            result = await session.execute(select(cls))
            return result.scalars().all()

    @classmethod
    async def update(cls, post_id, title, content, user_id):

        try:
            async with db_conn.session as session:
                query = select(cls).where(cls.id == post_id)
                result = await session.execute(query)
                post = result.scalar_one_or_none()

                if post:
                    post.title = title
                    post.content = content
                    session.add(post)
                    await session.commit()
                    return post
                else:
                    print(f"Post with id {post_id} not found")
                    return None
        except Exception as e:
            print(f"Error updating post: {e}")
            return None

    @classmethod
    async def delete(cls, post_id):
        async with db_conn.session as session:
            query = select(cls).where(cls.id == post_id)
            result = await session.execute(query)
            post = result.scalar_one_or_none()
            if post:
                await session.delete(post)
                await session.commit()
                return True
            else:
                return False
