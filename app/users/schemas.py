from pydantic import BaseModel, EmailStr


class SUser(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class SAuthor(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True