from pydantic import BaseModel


class Mail(BaseModel):
    email: str
    subject: str
    html_content: str
