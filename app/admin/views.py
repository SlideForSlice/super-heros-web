from sqladmin import  ModelView

from app.articles.model import Article
from app.chat_messages.model import ChatMessage
from app.support.model import Support
from app.users.model import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    column_details_exclude_list = [User.hashed_pass]
    can_delete = False
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

class ArticleAdmin(ModelView, model=Article):
    column_list = [Article.id, Article.name_of_hero, Article.author_id]
    can_delete = False
    name = "Article"
    name_plural = "Articles"
    icon = "fa-solid fa-document"

class SupportAdmin(ModelView, model=Support):
    column_list = [Support.chat_id, Support.chat_name, Support.user_id]
    can_delete = False
    name = "Support chat"
    name_plural = "Support chats"
    icon = "fa-solid fa-support"

class MessagesAdmin(ModelView, model=ChatMessage):
    column_list = [ChatMessage.message_id, ChatMessage.message, ChatMessage.chat_id, ChatMessage.user_id]
    can_delete = False
    name = "Message"
    name_plural = "Messages"
    icon = "fa-solid fa-mail"