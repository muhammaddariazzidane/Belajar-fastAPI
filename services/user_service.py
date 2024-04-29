from fastapi import HTTPException
from connection import engine
from schemas.user_schema import Users


async def find_user_by_email(email: str):
    try:
        user = await engine.find_one(Users, Users.email == email)
        return user
    except:
        raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan")
