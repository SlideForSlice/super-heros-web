from pydantic import BaseModel, EmailStr


class SUser(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class SAuthor(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True