import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy import insert
from typing_extensions import override

from app.config import settings
from app.database import Base, async_session_maker, engine

from app.users.model import User
from app.articles.model import Article
from app.support.model import Support
from app.chat_messages.model import ChatMessage
import aiofiles
from fastapi.testclient import TestClient
from app.main import create_app

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


    async def open_mock_json(model: str):
        mock_path = Path("mocks")
        file_path = mock_path /  f"mock_{model}.json"
        # if not mock_path.exists():
        #     raise FileNotFoundError(f"Mock file for model '{model}' not found: {mock_path}")

        async with aiofiles.open(file_path, mode="r", encoding="utf-8") as file:
            content = await file.read()
            return json.loads(content)

    users = await  open_mock_json("users")
    articles = await  open_mock_json("articles")
    support = await  open_mock_json("support")
    messages = await  open_mock_json("messages")

    for article in articles:
        article["created_at"] = datetime.strptime(article["created_at"], "%Y-%m-%d")
    for support_thing in support:
        support_thing["created_at"] = datetime.strptime(support_thing["created_at"], "%Y-%m-%dT%H:%M:%S")
    for message in messages:
        message["created_at"] = datetime.strptime(message["created_at"], "%Y-%m-%dT%H:%M:%S")


    async with async_session_maker() as session:
        await session.execute(insert(User).values(users))
        await session.execute(insert(Article).values(articles))
        await session.execute(insert(Support).values(support))
        await session.execute(insert(ChatMessage).values(messages))

        await session.commit()

@pytest.fixture(scope="session", autouse=True)
def ac():
    app = create_app()
    with TestClient(app) as ac:
        yield ac

@pytest_asyncio.fixture(scope="session", autouse=True)
async def session():
    async with async_session_maker() as session:
        yield session