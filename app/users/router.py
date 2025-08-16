from fastapi import APIRouter, Depends
from fastapi import Response

from app.exeptions import *
from app.users.dependecies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UserDao

router = APIRouter(
    prefix='/auth',
    tags=['Auth & Пользователи']
)


@router.post('/register')
async def register_user(user_Data: SUserAuth):
    existing_user = await UserDao.find_one_or_none(email=user_Data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_Data.password)
    await UserDao.add(email=user_Data.email, hashed_password=hashed_password)


@router.post('/login')
async def login_user(response: Response, user_Data: SUserAuth):
    user = await authenticate_user(user_Data.email, user_Data.password)
    if not user:
        raise IncorrectUserEmailOrPasswordException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return {'access_token': access_token}


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('booking_access_token')


@router.get('/me')
async def read_user_me(current_user: Users = Depends(get_current_user)):
    return current_user
