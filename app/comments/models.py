from datetime import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nick: Mapped[str] = mapped_column(String(15), nullable=True)
    text: Mapped[str] = mapped_column(String(1500), nullable=False)
    create_at: Mapped[datetime] = mapped_column(default=datetime.now)
    thread_id: Mapped[int] = mapped_column(index=True, nullable=False)

    media = relationship("CommentMedia", back_populates="comment", lazy="selectin")


class CommentMedia(Base):
    __tablename__ = "comments_media"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id"), index=True)
    filename:Mapped[str] =  mapped_column(String(150), nullable=False)

    comment = relationship(Comment, back_populates="media", lazy="selectin")
