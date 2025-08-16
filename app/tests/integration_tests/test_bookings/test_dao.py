import pytest

from app.bookings.dao import BookingDAO
from datetime import datetime


@pytest.mark.parametrize('user_id,room_id,date_from,date_to', [
    (5, 1, '2023-06-10', '2023-07-24'),
    (5, 1, '2023-06-10', '2023-07-24'),
    (5, 1, '2023-06-10', '2023-07-24'),
    (5, 3, '2023-06-10', '2023-07-24'),
])
async def test_add_and_get_booking(user_id, room_id, date_from, date_to):
    new_booking = await BookingDAO.add(
        user_id=user_id,
        room_id=room_id,
        date_from=datetime.strptime(date_from, '%Y-%m-%d'),
        date_to=datetime.strptime(date_to, '%Y-%m-%d')
    )

    assert new_booking.user_id == user_id
    assert new_booking.room_id == room_id

    new_booking = await BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None
