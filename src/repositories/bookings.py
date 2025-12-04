from datetime import date

from sqlalchemy import select

from src.exceptions import AllRoomsAreBookedException, validate_booking_dates
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd, Booking


class BookingsRepository(BaseRepository[BookingsOrm, Booking]):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(self.model).where(self.model.date_from == date.today())
        res = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, booking_data: BookingAdd, hotel_id: int):
        validate_booking_dates(date_from=booking_data.date_from, date_to=booking_data.date_to)
        query = rooms_ids_for_booking(
            date_from=booking_data.date_from, date_to=booking_data.date_to, hotel_id=hotel_id
        )
        result = await self.session.execute(query)
        availability_ids = result.scalars().all()
        if booking_data.room_id not in availability_ids:
            raise AllRoomsAreBookedException

        return await self.add(booking_data)
