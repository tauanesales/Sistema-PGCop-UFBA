from fastapi import APIRouter

from src.api.entrypoints.mailer.schema import Mail
from src.api.mailsender.mailer import Mailer

router = APIRouter()
mailer = Mailer()


@router.post("/send", status_code=200)
def send_message(mail: Mail):
    mailer.send_message(mail.email, mail.subject, mail.html_content)
