from fastapi import FastAPI
from app.users.router import router as users_router
from app.articles.router import router as articles_router
from app.support.router import router as support_router
from app.chat_messages.router import router as chat_messages_router

app = FastAPI()


app.include_router(users_router)
app.include_router(articles_router)
app.include_router(support_router)
app.include_router(chat_messages_router)


