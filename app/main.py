from idlelib.iomenu import encoding

from fastapi import FastAPI
from sqlalchemy.event import listens_for
from uvicorn import lifespan

from app.articles.router import router as articles_router
from app.chat_messages.router import router as chat_messages_router
from app.support.router import router as support_router
from app.users.router import router as users_router
from fastapi_versioning import VersionedFastAPI
# from starlette.middleware import Middleware
# from starlette.middleware.sessions import SessionMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from redis import asyncio as aioredis



@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url("redis://localhost:6379",encoding="utf8" , decode_responses=False)
    FastAPICache.init(
        RedisBackend(redis),
        prefix="cache")
    yield
    await redis.close()


app = FastAPI(lifespan=lifespan)



app.include_router(users_router, prefix="/v1")
app.include_router(articles_router, prefix="/v1")
app.include_router(support_router, prefix="/v1")
app.include_router(chat_messages_router, prefix="/v1")


# app = VersionedFastAPI(base_app,
#     version_format='{major}',
#     prefix_format='/v{major}',
#     # description='Greet users with a nice message',
#     # middleware=[
#     #     Middleware(SessionMiddleware, secret_key='mysecretkey')
#     # ]
# )
