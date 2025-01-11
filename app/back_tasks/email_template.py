from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_new_article_notification(
        article: dict,
        email_to: str
):
    email = EmailMessage()

    email["Subject"] = "You create a new Article"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>You create a new Article</h1>
            Congrats! That article: {article}
        """,
        subtype="html"
    )
    return email


