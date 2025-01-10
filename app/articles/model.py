from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Article(Base):
    __tablename__ = 'articles'


    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_of_hero: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    powers: Mapped[str] = mapped_column(String, nullable=False)
    solo: Mapped[bool] = mapped_column(Boolean, default=False)
    image: Mapped[str] = mapped_column(String, nullable=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    created_at: Mapped[date] = mapped_column(Date, nullable=False)

    author: Mapped['User'] = relationship('User', back_populates='articles')
