from typing import List, Dict

from fastapi import APIRouter
from fastapi.params import Depends

from app.chat_messages.dao import ChatMessageDAO
from app.chat_messages.schema import SChatMessage
from app.exceptions import *
from app.users.dependencies import get_current_user
from app.users.model import User

router = APIRouter(
    prefix="/chat_messages",
    tags=["chat_messages"],
)

@router.get("/all/{chat_id}")
async def get_all_messages_by_chat_id(chat_id: int) -> List[SChatMessage]:
    result = await ChatMessageDAO.find_all_with_filter(chat_id=chat_id)

    if not result:
        raise MessagesNotFound
    return result
@router.post("/{chat_id}")
async def create_chat_message(
        chat_id: int,
        message: str,
        user: User = Depends(get_current_user)
) -> SChatMessage:
    result = await ChatMessageDAO.add(chat_id=chat_id, message=message, user_id=user.id)
    if not result:
        raise MessagesNotFound
    return result

@router.patch("/{chat_message_id}")
async def update_chat_message(chat_message_id: int, message: str) -> SChatMessage:
    result = await ChatMessageDAO.update_message(message_id=chat_message_id, text=message)
    if not result:
        raise MessagesNotFound
    return result

@router.delete("/{chat_message_id}")
async def delete_chat_message(message_id: int) -> Dict[str, str]:
    result = await ChatMessageDAO.delete_message(message_id)
    if not result:
        raise MessagesNotFound
    return {"message": "The message was deleted"}

