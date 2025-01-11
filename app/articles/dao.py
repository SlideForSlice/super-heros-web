import shutil
from datetime import datetime, timezone
from pathlib import Path

from fastapi import UploadFile

from sqlalchemy import select
from sqlalchemy.exc import DatabaseError, IntegrityError

from app.articles.model import Article
from app.articles.schema import SArticles
from app.back_tasks.tasks import process_pic, send_notification
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import *
from app.users.model import User

UPLOAD_DIR = Path("app/images")
UPLOAD_DIR.mkdir(exist_ok=True)
BASE_URL = "http://localhost:8000"

class ArticleDAO(BaseDAO):
    model = Article

    @classmethod
    async def add(
            cls,
            name_of_hero: str,
            description: str,
            powers: str,
            solo: bool,
            author_id: int
    ):
        async with async_session_maker() as session:
            try:
                query = select(Article).where(Article.name_of_hero == name_of_hero)
                result = await session.execute(query)
                article_exists = result.scalar_one_or_none()



                if not article_exists:

                    created_at = datetime.now(timezone.utc).replace(tzinfo=None)

                    new_article = Article(
                        name_of_hero=name_of_hero,
                        description=description,
                        powers=powers,
                        solo=solo,
                        author_id=author_id,
                        created_at=created_at
                    )

                    session.add(new_article)
                    await session.commit()
                    await session.refresh(new_article)

                    query = select(User).where(User.id == author_id)
                    result = await session.execute(query)
                    user = result.scalar_one_or_none()

                    if not user:
                        # Если вдруг такого пользователя нет, бросаем ошибку или обрабатываем как-то иначе
                        raise DatabaseError(f"User with id={author_id} not found")

                    pydantic_article = SArticles.model_validate(new_article)
                    article_dict = pydantic_article.model_dump()
                    send_notification.delay(article_dict, user.email)

                    return new_article

                else:
                    raise ArticleIsAlreadyExistsException
            except IntegrityError as e:
                await session.rollback()
                raise DatabaseError(f"Database integrity error: {e}")

            except Exception as e:
                await session.rollback()
                raise DatabaseError(f"An error occurred while adding the article: {e}")

    @classmethod
    async def upload_file(
            cls,
            article_id: int,
            file: UploadFile
    ):
        if file.content_type not in ['image/jpeg', 'image/png']:
            raise UploadFileError

        file_path = UPLOAD_DIR / f'{article_id}_{file.filename}.jpg'

        try:
            with file_path.open('wb') as f:
                shutil.copyfileobj(file.file, f)

            process_pic.delay(str(file_path))

        except Exception as e:
            raise e

        async with async_session_maker() as session:
            try:
                query = select(Article).where(Article.id == article_id)
                result = await session.execute(query)
                article = result.scalar_one_or_none()

                if not article:
                    raise ArticleIsAlreadyExistsException

                article.image = str(file_path)
                await session.commit()
                await session.refresh(article)
                return article

            except IntegrityError as e:
                await session.rollback()
                raise DatabaseError(f"Database integrity error: {e}")

            except Exception as e:
                await session.rollback()
                raise DatabaseError(f"An error occurred while adding the article: {e}")


    @classmethod
    async def share_link(
            cls,
            article_id: int
    ):
        async with async_session_maker() as session:

            query = select(Article).where(Article.id == article_id)
            result = await session.execute(query)
            article = result.scalar_one_or_none()

            if not article:
                raise ArticleIsNotFound

            share_link = f"{BASE_URL}/articles/{article_id}"

            return share_link

    @classmethod
    async def get_author(
            cls,
            article_id: int
    ):

        async with async_session_maker() as session:
            try:
                query = (
                    select(User.id, User.email)
                    .join(Article, User.id == Article.author_id)
                    .where(Article.id == article_id)
                )
                result = await session.execute(query)
                author  = result.first()

                if not author:
                    raise UserDontFound

                return {"id": author.id, "email": author.email}

            except Exception as e:
                raise DatabaseError(f"An error occurred while retrieving the author: {e}")
