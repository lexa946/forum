from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import PG_HOST, PG_USER, PG_PASSWORD


class Base(DeclarativeBase):
    pass

engine = create_async_engine(f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}"
                             f"@{PG_HOST}:5432/forum", echo=True)
new_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

