import asyncio
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from app.comments.models import Comment, CommentMedia
from app.main import app as fastapi_application
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.threads.models import Thread
from app.s3.client import s3_client

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    def open_mock_json(suffix: str):
        with open(f"app/tests/mock_{suffix}.json", encoding="UTF-8") as file:
            return json.load(file)

    threads = open_mock_json("threads")
    comments = open_mock_json("comments")

    async with async_session_maker() as session:
        add_threads = insert(Thread).values(threads)
        await session.execute(add_threads)

        for comment_json in comments:
            comment = Comment(thread_id=comment_json['thread_id'],
                              text=comment_json['text'],
                              nick=comment_json['nick'],
            )

            session.add(comment)
            await session.flush()

            for file in comment_json['files']:
                file_path = Path(file)

                media = CommentMedia(comment_id=comment.id, filename=file_path.name)
                session.add(media)
                await session.flush()
                s3_url = await s3_client.upload_file(key=f"{media.id}_{media.filename}", body=file_path.read_bytes())
                media.s3_url = s3_url
                await session.flush()

        await session.commit()



@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()




@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(base_url="http://test", transport=ASGITransport(app=fastapi_application)) as aclient:
        yield aclient

@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session






