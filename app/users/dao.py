from app.DAO.base import BaseDAO
from app.users.models import Users


class UserDao(BaseDAO):
    model = Users
