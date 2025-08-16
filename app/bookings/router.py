from fastapi import APIRouter, Depends, status

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.models import Users
from app.users.dependecies import get_current_user
from datetime import date
from app.exeptions import RoomCannotBeBooked
from fastapi_versioning import version


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)


@router.get('')
@version(1)
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post('')
@version(1)
async def add_booking(
        room_id: int, date_from: date, date_to: date,
        user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked()

    return booking


@router.delete('/{booking_id}', status_code=status.HTTP_204_NO_CONTENT)
@version(1)
async def delete_booking(booking_id: int,
                         user: Users = Depends(get_current_user)
                         ):
    await BookingDAO.delete(id=booking_id, user_id=user.id)


