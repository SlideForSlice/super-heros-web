from sqlalchemy import delete, insert, select, update

from app.database import async_session_maker



class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            return user


    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update(cls, id: int, **kwargs):
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == id)
                .values(**kwargs)
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def delete(cls, id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            object = result.scalar_one_or_none()

            if object is not None:
                delete_query = delete(cls.model).where(cls.model.id == id)
                await session.execute(delete_query)
                await session.commit()
                return object
            else:
                return None
