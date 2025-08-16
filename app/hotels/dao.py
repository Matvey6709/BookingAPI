from app.DAO.base import BaseDAO
from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.models import Hotels
from datetime import date
from sqlalchemy import select, and_, or_, func

from app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(cls, location: str,
                       date_from: date,
                       date_to: date):
        '''
        :param location:
        :param date_from:
        :param date_to:
        :return:

        WITH booked_rooms AS(
            SELECT * from Bookings
            WHERE (date_from >= '2023-03-05' and date_from <= '2023-09-30')
            or (date_from <= '2023-03-05' and date_to > '2023-03-05')
        ),
        tbl AS(
            SELECT Rooms.id, Rooms.hotel_id, (Rooms.quantity-COUNT(booked_rooms.id)) as ost FROM Rooms
            LEFT JOIN booked_rooms ON Rooms.id=booked_rooms.room_id
            GROUP BY Rooms.id
            HAVING (Rooms.quantity-COUNT(booked_rooms.id)) > 0
            ORDER BY Rooms.id)

        SELECT Hotels.id, Hotels.name, Hotels.location, Hotels.services, Hotels.rooms_quantity,
        Hotels.image_id, SUM(tbl.ost) AS rooms_left FROM tbl
        JOIN Hotels ON tbl.hotel_id=Hotels.id
        WHERE Hotels.location LIKE '%Алтай%'
        GROUP BY Hotels.id
        '''
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        ),
                    )
                )
            ).cte('booked_rooms')

            tbl_info = select(Rooms.id, Rooms.hotel_id, (Rooms.quantity - func.count(booked_rooms.c.id)).label('ost')
                              ).select_from(Rooms).outerjoin(booked_rooms, Rooms.id == booked_rooms.c.room_id
                                                             ).group_by(Rooms.id).having(
                (Rooms.quantity - func.count(booked_rooms.c.id)) > 0
            ).order_by(Rooms.id).cte('tbl_info')

            res = select(Hotels.id, Hotels.name, Hotels.location, Hotels.services, Hotels.rooms_quantity,
                         Hotels.image_id, func.sum(tbl_info.c.ost).label('rooms_left')).select_from(tbl_info
                                                                                                    ).join(Hotels,
                                                                                                           tbl_info.c.hotel_id == Hotels.id).where(
                Hotels.location.like(f'%{location}%')
            ).group_by(Hotels.id)

            rooms_left = await session.execute(res)
            return rooms_left.mappings().all()

    @classmethod
    async def search_for_rooms(
            cls,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        '''
        :param hotel_id:
        :param date_from:
        :param date_to:
        :return:
        WITH booked_rooms AS(
            SELECT * from Bookings
            WHERE (date_from >= '2023-03-05' and date_from <= '2023-09-30')
            or (date_from <= '2023-03-05' and date_to > '2023-03-05')
        )
        SELECT Rooms.id, Rooms.hotel_id, Rooms.name, Rooms.description, Rooms.services,
        Rooms.price, Rooms.quantity, Rooms.image_id,
        Rooms.price * ('2023-03-25'::date - '2023-03-05'::date) AS total_cost,
        (Rooms.quantity-COUNT(booked_rooms.id)) as rooms_left FROM Rooms
        LEFT JOIN booked_rooms ON Rooms.id=booked_rooms.room_id
        GROUP BY Rooms.id
        HAVING (Rooms.quantity-COUNT(booked_rooms.id)) > 0 and Rooms.hotel_id = 1
        ORDER BY Rooms.id
        '''
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        ),
                    )
                )
            ).cte('booked_rooms')
            res = select(Rooms.id, Rooms.hotel_id, Rooms.name, Rooms.description, Rooms.services,
            Rooms.price, Rooms.quantity, Rooms.image_id, (Rooms.price * (date_to - date_from).days).label('total_cost'),
                         (Rooms.quantity - func.count(booked_rooms.c.id)).label('rooms_left')
                              ).select_from(Rooms).outerjoin(booked_rooms, Rooms.id == booked_rooms.c.room_id
                                                             ).group_by(Rooms.id).having(
                and_((Rooms.quantity - func.count(booked_rooms.c.id)) > 0, Rooms.hotel_id == hotel_id)
            ).order_by(Rooms.id)


            rooms_left = await session.execute(res)
            return rooms_left.mappings().all()
