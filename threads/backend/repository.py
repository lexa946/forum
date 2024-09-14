from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from schemas.main import SThreadAdd, SThread, SPaginator
from backend.db import new_session

from models.main import Thread


class ThreadRepository:

    @classmethod
    async def add_thread(cls, add_thread: SThreadAdd) -> SThread:
        async with new_session() as session:
            session: AsyncSession
            thread = Thread(**add_thread.model_dump())
            session.add(thread)
            await session.flush()
            await session.commit()
            return SThread.model_validate(thread)

    @classmethod
    async def get_thread(cls, id_: int) -> SThread:
        async with new_session() as session:
            session: AsyncSession

            thread = await session.scalar(
                select(Thread).where(Thread.id == id_)
            )
            if not thread:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Thread with {id_=} not found!"
                )
            return SThread.model_validate(thread)

    @classmethod
    async def get_threads(cls, paginator: SPaginator) -> list[SThread]:
        async with new_session() as session:
            session: AsyncSession

            query = await session.scalars(
                select(Thread).order_by(Thread.create_at).offset(paginator.offset).limit(
                    paginator.limit)
            )

            threads = query.all()
            return [SThread.model_validate(thread) for thread in threads]
