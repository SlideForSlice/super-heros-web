from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Support(Base):
    __tablename__ = 'support'

    chat_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_name: Mapped[str] = mapped_column(String, nullable=False)
    is_solved: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())

    user: Mapped['User'] = relationship('User', back_populates='support')
    messages: Mapped[list['ChatMessage']] = relationship('ChatMessage', back_populates='chat')