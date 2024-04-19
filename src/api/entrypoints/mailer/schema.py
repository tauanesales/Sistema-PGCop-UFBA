from pydantic import BaseModel
from typing import Optional


class Mail(BaseModel):
    email: str
    subject: str
    html_content: str