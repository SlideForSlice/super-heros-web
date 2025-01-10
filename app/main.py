from fastapi import FastAPI

from app.articles.router import router as articles_router
from app.chat_messages.router import router as chat_messages_router
from app.support.router import router as support_router
from app.users.router import router as users_router
from fastapi_versioning import VersionedFastAPI
# from starlette.middleware import Middleware
# from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()


app.include_router(users_router)
app.include_router(articles_router)
app.include_router(support_router)
app.include_router(chat_messages_router)

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    # description='Greet users with a nice message',
    # middleware=[
    #     Middleware(SessionMiddleware, secret_key='mysecretkey')
    # ]
)
