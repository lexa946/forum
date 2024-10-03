from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id == model_id)
            result = await session.scalar(query)
            return result


    @classmethod
    async def find_one_or_none(cls, **filters_by):
        async with async_session_maker() as session:
            session: AsyncSession
            query = select(cls.model).filter_by(**filters_by)
            result = await session.scalar(query)
            return result

    @classmethod
    async def find_all(cls, limit=0, offset=0, order_by="desc", **filters_by) -> list[model]:
        async with async_session_maker() as session:

            query = select(cls.model).filter_by(**filters_by)
            if order_by == "desc":
                query = query.order_by(cls.model.create_at.desc())
            else:
                query = query.order_by(cls.model.create_at.asc())

            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)
            result = await session.scalars(query)
            return result.all()


    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            item  = cls.model(**data)
            session.add(item)
            await session.commit()
            return item

    @classmethod
    async def delete(cls, model_id):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(id=model_id)
            await session.execute(query)
            await session.commit()
