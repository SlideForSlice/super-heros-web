from typing import Optional

from pydantic import BaseModel
from datetime import date, datetime


class SSupport(BaseModel):
    chat_id: int
    chat_name: str
    is_solved: bool
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True







