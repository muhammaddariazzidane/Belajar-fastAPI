from typing import Optional
from odmantic import Model, Field


class Users(Model):
    username: str
    email: str = Field(unique=True)
    password: str
    avatar: Optional[str] = None
