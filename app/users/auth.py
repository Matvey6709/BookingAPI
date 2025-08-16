import logging
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.users.dao import UserDao
from app.config import Secret_JWT_KEY, ALGORITM

pwd_context = CryptContext(schemes=['bcrypt'])
logging.getLogger('passlib').setLevel(logging.ERROR)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, Secret_JWT_KEY, ALGORITM
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UserDao.find_one_or_none(email=email)
    if not (user and verify_password(password, user.hashed_password)):
        return None
    return user
