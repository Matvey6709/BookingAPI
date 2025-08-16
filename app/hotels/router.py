import datetime

from fastapi import APIRouter, Query

from app.hotels.dao import HotelDAO
from datetime import date
from fastapi_cache.decorator import cache

from app.hotels.rooms.schemas import RoomInfo
from app.hotels.schemas import SHotels

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get('/{location}')
@cache(expire=60)
async def get_hotels_by_location_and_time(
        location: str,
        date_from: date = Query(..., description=f'Например, {datetime.datetime.now().date()}'),
        date_to: date = Query(..., description=f'Например, {datetime.datetime.now().date()}')
) -> list[SHotels]:
    return await HotelDAO.find_all(location=location, date_from=date_from, date_to=date_to)


@router.get('/id/{hotel_id}')
async def get_hotel(hotel_id: int) -> SHotels:
    return await HotelDAO.find_one_or_none(id=hotel_id)


@router.get('/{hotel_id}/rooms')
async def get_rooms_by_time(
        hotel_id: int,
        date_from: date = Query(..., descriptions=f'Например, {datetime.datetime.now().date()}'),
        date_to: date = Query(..., descriptions=f'Например, {datetime.datetime.now().date()}')
) -> list[RoomInfo]:
    return await HotelDAO.search_for_rooms(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
