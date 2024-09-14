from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from schemas.main import SCommentAdd, SComment
from backend.db import new_session

from models.main import Comment


class CommentRepository:

    @classmethod
    async def add_comment(cls, add_comment: SCommentAdd) -> SComment:
        async with new_session() as session:
            session: AsyncSession
            thread = Comment(**add_comment.model_dump())
            session.add(thread)
            await session.flush()
            await session.commit()
            return SComment.model_validate(thread)

    @classmethod
    async def get_comment(cls, id_: int) -> SComment:
        async with new_session() as session:
            session: AsyncSession

            comment = await session.scalar(
                select(Comment).where(Comment.id == id_)
            )
            if not comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Thread with {id_=} not found!"
                )
            return SComment.model_validate(comment)

    @classmethod
    async def get_comments(cls, thread_id: int, offset: int = 0, limit: int = 20) -> list[SComment]:
        async with new_session() as session:
            session: AsyncSession

        query = await session.scalars(
            select(Comment).where(Comment.thread_id == thread_id).order_by(Comment.create_at).offset(offset).limit(
                limit)
        )
        comments = query.all()
        return [SComment.model_validate(comment) for comment in comments]
