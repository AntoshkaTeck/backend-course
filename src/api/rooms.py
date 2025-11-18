from datetime import date

from fastapi import APIRouter, Body, Query, HTTPException
from fastapi.openapi.models import Example

from src.api.dependencies import DBDep
from src.exceptions import (
    IncorrectDatesException,
    RoomNotFoundHTTPException,
    HotelNotFoundHTTPException,
    HotelNotFoundException,
    RoomNotFoundException,
    RoomEmptyFieldsException,
    RoomEmptyFieldsHTTPException,
    RoomFacilityNotFoundException,
    RoomFacilityNotFoundHTTPException,
)
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest, Room, RoomWithRels
from src.service.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get(
    "/{hotel_id}/rooms",
    summary="Получить все номера по id отеля",
    response_model=list[RoomWithRels],
)
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(openapi_examples={"default": Example(value="2025-10-21")}),
    date_to: date = Query(openapi_examples={"default": Example(value="2025-10-24")}),
):
    try:
        res = await RoomService(db).get_filtered_by_date(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
        return res
    except IncorrectDatesException as ex:
        raise HTTPException(status_code=400, detail=ex.detail)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить один номер", response_model=Room)
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await RoomService(db).get_room(room_id=room_id, hotel_id=hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms", summary="Добавить номер", response_model=Room)
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
                },
            ),
            "2": Example(
                summary="Империал",
                value={
                    "title": "Номер империал с собственным бассейном",
                    "description": "Роскошный номер, с собственным бассейном и выходом к морю",
                    "price": 5000,
                    "quantity": 2,
                    "facilities_ids": [],
                },
            ),
        }
    ),
):
    try:
        return await RoomService(db).create_room(hotel_id=hotel_id, room_data=room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomFacilityNotFoundException:
        raise RoomFacilityNotFoundHTTPException


@router.put(
    "/{hotel_id}/rooms/{room_id}", summary="Изменить инфо номера (все поля)", response_model=Room
)
async def update_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    try:
        return await RoomService(db).update_room(
            hotel_id=hotel_id, room_id=room_id, room_data=room_data
        )
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except RoomFacilityNotFoundException:
        raise RoomFacilityNotFoundHTTPException


@router.patch(
    "/{hotel_id}/rooms/{room_id}", summary="Изменить инфо номера (частично)", response_model=Room
)
async def update_room_partially(
    db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest
):
    try:
        return await RoomService(db).update_room_partially(
            hotel_id=hotel_id, room_id=room_id, room_data=room_data
        )
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except RoomEmptyFieldsException:
        raise RoomEmptyFieldsHTTPException
    except RoomFacilityNotFoundException:
        raise RoomFacilityNotFoundHTTPException


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await RoomService(db).delete_room(hotel_id=hotel_id, room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"satus": "OK"}
