from src.exceptions import AllRoomsAreBookedException
from src.schemas.bookings import BookingAddRequest, BookingAdd, Booking
from src.service.base import BaseService
from src.service.hotels import HotelService
from src.service.rooms import RoomService


class BookingService(BaseService):
    async def create_booking(self, user_id: int, booking_data: BookingAddRequest) -> Booking:
        room = await RoomService(self.db).get_room_and_check(room_id=booking_data.room_id)
        hotel = await HotelService(self.db).get_hotel_and_check(room.hotel_id)
        _booking_data = BookingAdd(user_id=user_id, **booking_data.model_dump(), price=room.price)
        try:
            booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        except AllRoomsAreBookedException as ex:
            raise ex
        await self.db.commit()
        return booking

    async def get_bookings(self) -> list[Booking]:
        return await self.db.bookings.get_all()

    async def get_bookings_current_user(self, user_id: int) -> list[Booking]:
        return await self.db.bookings.get_filtered(user_id=user_id)
