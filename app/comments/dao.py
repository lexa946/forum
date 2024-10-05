from fastapi import UploadFile
from sqlalchemy import select


from app.comments.models import Comment, CommentMedia
from app.comments.schemas import SCommentAdd
from app.dao.base import BaseDAO
from app.database import async_session_maker

from app.s3.client import s3_client

class CommentDAO(BaseDAO):
    model = Comment

    @classmethod
    async def add(cls, comment: SCommentAdd, files:list[UploadFile]=None,):
        async with async_session_maker() as session:
            comment = Comment(**comment.model_dump())
            session.add(comment)
            await session.flush()


            if files:
                for file in files:
                    media = CommentMedia(comment_id=comment.id, filename=file.filename)
                    session.add(media)
                    await session.flush()
                    s3_url = await s3_client.upload_file(key=f"{media.id}_{media.filename}", body=file.file)
                    media.s3_url = s3_url

            await session.commit()
            comment = await session.scalar(select(Comment).where(Comment.id == comment.id))
            return comment