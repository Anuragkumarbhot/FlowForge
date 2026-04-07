from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from app.db.database import users_collection

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"])

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


def create_token(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register")
async def register(user: dict):

    existing = await users_collection.find_one(
        {"email": user["email"]}
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    user["password"] = hash_password(
        user["password"]
    )

    await users_collection.insert_one(user)

    return {"message": "User created"}


@router.post("/login")
async def login(user: dict):

    db_user = await users_collection.find_one(
        {"email": user["email"]}
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        user["password"],
        db_user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_token(user["email"])

    return {"access_token": token}
