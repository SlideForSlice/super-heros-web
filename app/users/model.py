from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.articles.model import Article
from app.chat_messages.model import ChatMessage
from app.database import Base
from app.support.model import Support


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_pass: Mapped[str] = mapped_column(String, nullable=False)

    articles: Mapped[list['Article']] = relationship('Article', back_populates='author')
    support: Mapped[list['Support']] = relationship('Support', back_populates='user')
    chat_messages: Mapped[list['ChatMessage']] = relationship('ChatMessage', back_populates='user')

    def __str__(self):
        return f"User: {self.email}"