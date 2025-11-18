from src.exceptions import (
    IncorrectDatesException,
    IncorrectDatesHTTPException,
    InvalidBookingDatesException,
    InvalidBookingDatesHTTPException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    AllRoomsAreBookedException,
    AllRoomsAreBookedHTTPException,
    ExpiredTokenException,
    ExpiredTokenHTTPException,
)


def register_exception_handlers(app):
    @app.exception_handler(IncorrectDatesException)
    async def incorrect_dates_handler(_, exc):
        raise IncorrectDatesHTTPException()

    @app.exception_handler(InvalidBookingDatesException)
    async def invalid_booking_dates_handler(_, exc):
        raise InvalidBookingDatesHTTPException()

    @app.exception_handler(RoomNotFoundException)
    async def room_not_found_handler(_, exc):
        raise RoomNotFoundHTTPException()

    @app.exception_handler(AllRoomsAreBookedException)
    async def all_rooms_booked_handler(_, exc):
        raise AllRoomsAreBookedHTTPException()

    @app.exception_handler(ExpiredTokenException)
    async def expired_token_handler(_, exc):
        raise ExpiredTokenHTTPException()
