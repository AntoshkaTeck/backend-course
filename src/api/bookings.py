from fastapi import APIRouter, Body, HTTPException
from fastapi.openapi.models import Example

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import ObjectNotFoundException
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
                value={"date_from": "2025-10-21", "date_to": "2025-10-24", "room_id": 5},
            )
        }
    ),
):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    hotel = await db.hotels.get_one(id=room.hotel_id)
    _booking_data = BookingAdd(user_id=user_id, **booking_data.model_dump(), price=room.price)
    booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    await db.commit()

    return {"status": "OK", "data": booking}


@router.get("/", summary="Получение всех бронирований")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Получение бронирований текущего пользователя")
async def get_bookings_current_user(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)
