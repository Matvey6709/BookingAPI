from datetime import datetime

from fastapi import Request, Depends
from jose import jwt, JWTError

from app.config import Secret_JWT_KEY, ALGORITM
from app.exeptions import TokenAbsentException, IncorrectTokenFormatException, TokenExpiredException, \
    UserIsNotPresentException
from app.users.dao import UserDao


def get_token(requests: Request):
    token = requests.cookies.get('booking_access_token')
    if not token:
        raise TokenAbsentException()
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, Secret_JWT_KEY, ALGORITM
        )
    except JWTError:
        raise IncorrectTokenFormatException()
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException()
    user_id: str = payload.get('sub')
    if not user_id:
        raise UserIsNotPresentException()
    user = await UserDao.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException()
    return user
