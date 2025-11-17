from fastapi import APIRouter, Body
from fastapi.openapi.models import Example

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.bookings import BookingAddRequest, Booking
from src.service.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("/", summary="Добавление бронирования", response_model=Booking)
async def create_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest = Body(
        openapi_examples={
            "1": Example(
                summary="Бронирование Люкс 3 ночи",
                value={"date_from": "2025-10-21", "date_to": "2025-10-24", "room_id": 5},
            )
        }
    ),
):
    return await BookingService(db).create_booking(user_id=user_id, booking_data=booking_data)


@router.get("/", summary="Получение всех бронирований", response_model=list[Booking])
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get(
    "/me", summary="Получение бронирований текущего пользователя", response_model=list[Booking]
)
async def get_bookings_current_user(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_bookings_current_user(user_id=user_id)
