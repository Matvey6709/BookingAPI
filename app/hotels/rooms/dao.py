from app.DAO.base import BaseDAO
from app.hotels.rooms.models import Rooms


class RoomDAO(BaseDAO):
    model = Rooms

