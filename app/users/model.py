from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_pass: Mapped[str] = mapped_column(String, nullable=False)

    articles: Mapped[list['Article']] = relationship('Article', back_populates='author')
    support: Mapped[list['Support']] = relationship('Support', back_populates='user')
    chat_messages: Mapped[list['ChatMessage']] = relationship('ChatMessage', back_populates='user')