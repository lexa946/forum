from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.db import Base


class Thread(Base):
    __tablename__ = 'threads'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    text: Mapped[str] = mapped_column(String(1500), nullable=False)
    create_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    nick: Mapped[str] = mapped_column(String(15), nullable=True)
