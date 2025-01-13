
from datetime import datetime, timezone

from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt

from app.config import settings
from app.exceptions import *
from app.users.dao import UserDAO


def get_token(request:Request) -> str:
    """Извлекает JWT-токен из куки."""
    token = request.cookies.get('user_access_token')
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(token: str = Depends(get_token)):
    """Возвращает текущего пользователя на основе JWT-токена."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.encode('utf-8'),
            algorithms=[settings.ALGORITHM]
        )
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException

    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpiredException

    user_id: str = payload.get('sub')
    if not user_id:
        raise UserIsNotPresentException

    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user
