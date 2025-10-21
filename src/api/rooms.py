from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi.openapi.models import Example

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получить все номера по id отеля")
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2025-10-21"),
        date_to: date = Query(example="2025-10-24"),
):
    return await db.rooms.get_filtered_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить один номер")
async def get_room(db: DBDep, hotel_id, room_id: int):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Добавить номер")
async def create_room(
        hotel_id: int,
        db: DBDep,
        room_data: RoomAddRequest = Body(
            openapi_examples={
                "1": Example(
                    summary="Люкс",
                    value={
                        "title": "Номер люкс с видом на гору",
                        "description": "Хороший номер с балконом",
                        "price": 1000,
                        "quantity": 10,
                        "facilities_ids": [],
                    }
                ),
                "2": Example(
                    summary="Империал",
                    value={
                        "title": "Номер империал с собственным бассейном",
                        "description": "Роскошный номер, с собственным бассейном и выходом к морю",
                        "price": 5000,
                        "quantity": 2,
                        "facilities_ids": [],
                    }
                )
            }
        ),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"satus": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменить инфо номера (все поля)")
async def update_room(db: DBDep, hotel_id:int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.update(_room_data, id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"satus": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Изменить инфо номера (частично)")
async def update_room_part(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.update(room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"satus": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"satus": "OK"}
