from fastapi import APIRouter, Body
from fastapi.openapi.models import Example

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получить все номера по id отеля")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)

@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить один номер")
async def get_room(hotel_id, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Добавить номер")
async def create_room(
        hotel_id: int,
        room_data: RoomAddRequest = Body(
            openapi_examples={
                "1": Example(
                    summary="Люкс",
                    value={
                        "title": "Номер люкс с видом на гору",
                        "description": "Хороший номер с балконом",
                        "price": 1000,
                        "quantity": 10
                    }
                ),
                "2": Example(
                    summary="Империал",
                    value={
                        "title": "Номер империал с собственным бассейном",
                        "description": "Роскошный номер, с собственным бассейном и выходом к морю",
                        "price": 5000,
                        "quantity": 2
                    }
                )
            }
        ),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()

    return {"satus": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменить инфо номера (все поля)")
async def update_room(hotel_id:int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).update(_room_data, id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {"satus": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Изменить инфо номера (частично)")
async def update_room_part(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).update(room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {"satus": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {"satus": "OK"}
