from sqlalchemy.exc import IntegrityError, DatabaseError

from app.chat_messages.model import ChatMessage
from app.dao.base import BaseDAO
from app.database import async_session_maker
from sqlalchemy import select, delete

from app.exceptions import MessagesNotFound


class ChatMessageDAO(BaseDAO):
    model = ChatMessage

    @classmethod
    async def add(
            cls,
            chat_id: int,
            message: str,
            user_id: int,
    ):
        async with async_session_maker() as session:
            try:

                new_message = ChatMessage(
                    chat_id=chat_id,
                    message=message,
                    user_id=user_id
                )
                session.add(new_message)
                await session.commit()
                await session.refresh(new_message)
                return new_message

            except IntegrityError as e:
                await session.rollback()
                raise DatabaseError(f"Database integrity error: {e}")

            except Exception as e:
                await session.rollback()
                raise DatabaseError(f"An error occurred while adding the article: {e}")

    @classmethod
    async def update_message(
            cls,
            message_id: int,
            text: str
    ):
        async with async_session_maker() as session:
            try:
                query = select(ChatMessage).where(ChatMessage.message_id == message_id)
                result = await session.execute(query)
                message = result.scalar_one_or_none()

                if not message:
                    raise MessagesNotFound

                message.message = text
                await session.commit()
                await session.refresh(message)
                return message

            except IntegrityError as e:
                await session.rollback()
                raise DatabaseError(f"Database integrity error: {e}")

            except Exception as e:
                await session.rollback()
                raise DatabaseError(f"An error occurred while adding the article: {e}")

    @classmethod
    async def delete_message(
            cls,
            message_id: int
    ):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(message_id=message_id)
            result = await session.execute(query)
            object = result.scalar_one_or_none()

            if object is not None:
                delete_query = delete(cls.model).where(cls.model.message_id == message_id)
                await session.execute(delete_query)
                await session.commit()
                return object
            else:
                return None
