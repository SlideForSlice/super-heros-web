from sqlalchemy.exc import IntegrityError, DatabaseError

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import *
from app.support.model import Support
from sqlalchemy import select, delete


class SupportDAO(BaseDAO):
    model = Support

    @classmethod
    async def add(
            cls,
            user_id: int,
            name: str
    ):
        async with async_session_maker() as session:
            try:

                new_support = Support(
                    chat_name=name,
                    user_id=user_id
                )
                session.add(new_support)
                await session.commit()
                await session.refresh(new_support)
                return new_support

            except IntegrityError as e:
                await session.rollback()
                raise DatabaseError(f"Database integrity error: {e}")

            except Exception as e:
                await session.rollback()
                raise DatabaseError(f"An error occurred while adding the article: {e}")

    @classmethod
    async def update_status(
            cls,
            chat_id: int,
            is_solved: bool
    ):

        async with async_session_maker() as session:
            try:
                query = select(Support).where(Support.chat_id == chat_id)
                result = await session.execute(query)
                support = result.scalar_one_or_none()

                if not support:
                    raise ChatNotFound

                support.is_solved = is_solved
                await session.commit()
                await session.refresh(support)
                return support

            except IntegrityError as e:
                await session.rollback()
                raise DatabaseError(f"Database integrity error: {e}")

            except Exception as e:
                await session.rollback()
                raise DatabaseError(f"An error occurred while adding the article: {e}")

    @classmethod
    async def delete_chat(
            cls,
            chat_id: int
    ):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(chat_id=chat_id)
            result = await session.execute(query)
            object = result.scalar_one_or_none()

            if object is not None:
                delete_query = delete(cls.model).where(cls.model.chat_id == chat_id)
                await session.execute(delete_query)
                await session.commit()
                return object
            else:
                return None



