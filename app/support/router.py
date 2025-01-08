from typing import List, Dict

from fastapi import APIRouter
from fastapi.params import Depends

from app.exceptions import *
from app.support.dao import SupportDAO
from app.support.schemas import SSupport
from app.users.dependencies import get_current_user
from app.users.model import User

router = APIRouter(
    prefix="/support",
    tags=["support"]
)

@router.get("/all_chats")
async def get_all_chats(current_user: User = Depends(get_current_user)) -> List[SSupport]:
    return await SupportDAO.find_all_with_filter(user_id=current_user.id)

@router.get("/{chat_id}")
async def get_chat_by_id(chat_id: int) -> SSupport:
    result = await SupportDAO.find_one_or_none(chat_id=chat_id)

    if not result:
        raise ChatNotFound
    else:
        return result

@router.post("/")
async def create_chat(
        chat_name: str,
        user: User = Depends(get_current_user)
) -> SSupport:
    return await SupportDAO.add(user_id=user.id, name=chat_name)

@router.patch("/{chat_id}")
async def update_status_chat(chat_id: int, is_solved: bool) -> SSupport:
    result = await SupportDAO.update_status(chat_id=chat_id, is_solved=is_solved)

    if not result:
        raise ChatNotFound
    else:
        return result

@router.delete("/{chat_id}")
async def delete_chat_by_id(chat_id: int) -> Dict[str, str]:
    result = await SupportDAO.delete_chat(chat_id=chat_id)

    if not result:
        raise ChatNotFound
    else:
        return {"message": "Chat was deleted"}