import smtplib
from email.message import EmailMessage

from pydantic import EmailStr

from app.back_tasks.celery import celery
from PIL import Image
from pathlib import Path
from smtplib import SMTP

from app.back_tasks.email_template import create_new_article_notification
from app.config import settings


@celery.task
def process_pic(
        path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_200_100 = im.resize((200, 100))
    im_resized_1000_500.save(f"app/images/resized_1000_500_{im_path.name}")
    im_resized_200_100.save(f"app/images/resized_200_100_{im_path.name}")


@celery.task
def send_notification(
        article: dict,
        email_to: str
):
    email_to_mock = settings.SMTP_USER
    msg_content = create_new_article_notification(article, email_to_mock)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
