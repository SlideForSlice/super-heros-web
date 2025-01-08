import logging

from fastapi import APIRouter, Response, Depends

from app.exceptions import *
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.model import User
from app.users.schemas import SUser

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/auth",
    tags=["auth & user"],
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: SUser):
    """Регистрация нового пользователя."""
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        logger.warning(f"User with email {user_data.email} already exists")
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_pass=hashed_password)
    logger.info(f"User with email {user_data.email} registered successfully")
    return {"message": "User registered successfully"}

@router.post("/login")
async def login_user(response: Response, user_data: SUser):
    """Аутентификация пользователя и выдача токена."""
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        logger.warning(f"Failed login attempt for email {user_data.email}")
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    logger.info(f"User with email {user_data.email} logged in successfully")
    return {"access_token": access_token}

@router.post("/logout")
async def logout_user(response: Response):
    """Выход пользователя и удаление токена."""
    response.delete_cookie("booking_access_token")
    logger.info("User logged out successfully")
    return {"message": "Logged out successfully"}

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Получение информации о текущем пользователе."""
    if current_user:
        return current_user
    else:
        logger.warning("Can't get user info")
        raise UserIsNotPresentException

