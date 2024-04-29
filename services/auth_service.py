from typing import Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv
from connection import engine
import os
from services.user_service import find_user_by_email
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(email: str, password: str):
    user = await find_user_by_email(email)
    if user and password_context.verify(password, user.password):
        return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM")
    )
    return encoded_jwt


async def create_user(user):
    hashed_password = password_context.hash(user.password)
    user.password = hashed_password
    if user.avatar:
        await engine.save(user)
    else:
        user.avatar = f"{os.getenv('AVATAR_API_URL')}/{user.username}.svg?apikey={os.getenv('AVATAR_API_KEY')}"
        await engine.save(user)
    return user
