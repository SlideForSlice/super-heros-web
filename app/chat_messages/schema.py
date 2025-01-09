from typing import Optional

from pydantic import BaseModel
from datetime import date, datetime


class SChatMessage(BaseModel):
    message_id: int
    chat_id: int
    user_id: int
    message: str
    created_at: datetime

    class Config:
        from_attributes = True