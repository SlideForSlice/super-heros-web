from datetime import date
from typing import Optional

from pydantic import BaseModel


class SArticles(BaseModel):
    id: int
    name_of_hero: str
    description: str
    powers: str
    solo: bool
    image: Optional[str] = None
    author_id: int
    created_at: date

    class Config:
        from_attributes = True