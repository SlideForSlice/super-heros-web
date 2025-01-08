from datetime import datetime, date

from sqlalchemy import Integer, String, ForeignKey, DateTime, Date, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class ChatMessage(Base):
    __tablename__ = 'chat_messages'

    message_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey('support.chat_id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    message: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())

    user: Mapped['User'] = relationship('User', back_populates='chat_messages')
    chat: Mapped['Support'] = relationship('Support', back_populates='messages')