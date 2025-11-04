from datetime import date

from fastapi import HTTPException
from sqlalchemy import select

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(self.model)
            .where(self.model.date_from == date.today())
        )
        res = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, booking_data: BookingAdd):
        query = rooms_ids_for_booking(
            date_from=booking_data.date_from,
            date_to=booking_data.date_to,
        )
        result = await self.session.execute(query)
        availability_ids = result.scalars().all()
        if booking_data.room_id not in availability_ids:
            raise HTTPException(status_code=403, detail="Бронирование запрещено")

        return await self.add(booking_data)
