from fastapi import APIRouter, Body
from fastapi.openapi.models import Example

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.post("/", summary="Добавление бронирования")
async def create_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest = Body(
            openapi_examples={
                "1": Example(
                    summary="Бронирование Люкс 3 ночи",
                    value={
                        "date_from": "2025-10-21",
                        "date_to": "2025-10-24",
                        "room_id": 5
                    }
                )
            }
        )
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    _booking_data = BookingAdd(user_id=user_id, **booking_data.model_dump(), price=room.price)
    booking = await db.bookings.add_booking(_booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}


@router.get("/bookings", summary="Получение всех бронирований")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/bookings/me", summary="Получение бронирований текущего пользователя")
async def get_bookings_current_user(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)