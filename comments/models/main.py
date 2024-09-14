from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.db import Base


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nick: Mapped[str] = mapped_column(String(15), nullable=True)
    text: Mapped[str] = mapped_column(String(1500), nullable=False)
    create_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    thread_id: Mapped[int] = mapped_column(index=True, nullable=False)