from services.auth_service import create_user, authenticate_user, create_access_token
import uvicorn
from odmantic import Model
from connection import engine
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
from services.user_service import find_user_by_email
from pymongo.errors import PyMongoError
from schemas.user_schema import Users

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    users_data = await engine.find(Users)
    return {"users": users_data}


@app.post("/login")
async def login(user: Users):
    auth_user = await authenticate_user(user.email, user.password)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token_expires = timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {
        "message": "Login Berhasil",
        "user": auth_user,
        "token": access_token,
    }


@app.post("/register")
async def register(user: Users):
    try:
        existing_user = await find_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email sudah terdaftar")
        await create_user(user)
        return {"message": "Registrasi Berhasil"}
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
