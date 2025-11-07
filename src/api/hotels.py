from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException
from fastapi.openapi.models import Example
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import IncorrectDatesException, ObjectNotFoundException, HotelNotFoundHTTPException
from src.schemas.hotels import HotelPatch, HotelAdd, Hotel
from src.service.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/", response_model=list[Hotel])
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        date_from: date = Query(openapi_examples={"default": Example(value="2025-10-21")}),
        date_to: date = Query(openapi_examples={"default": Example(value="2025-10-24")}),
        title: str | None = Query(default=None, description="Название отеля"),
        location: str | None = Query(default=None, description="Расположение отеля"),
):
    try:
        return await HotelService(db).get_filtered_by_date(
            pagination=pagination,
            date_from=date_from,
            date_to=date_to,
            title=title,
            location=location,
        )
    except IncorrectDatesException as ex:
        raise HTTPException(status_code=400, detail=ex.detail)


@router.get("/{hotel_id}", summary="Получить один отель", response_model=Hotel)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("/", response_model=Hotel)
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(
            openapi_examples={
                "1": Example(
                    summary="Сочи", value={"title": "Отель Сочи 5 звезд", "location": "ул. Моря 1"}
                ),
                "2": Example(
                    summary="Дубай", value={"title": "Отель Дубай у фонтана", "location": "ул. Шейха 2"}
                ),
            }
        ),
):
    return await HotelService(db).create_hotel(hotel_data=hotel_data)


@router.put("/{hotel_id}", response_model=Hotel)
async def update_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    return await HotelService(db).update_hotel(hotel_data=hotel_data, hotel_id=hotel_id)


@router.patch("/{hotel_id}", response_model=Hotel)
async def update_hotel_partially(
        hotel_id: int,
        hotel_data: HotelPatch,
        db: DBDep,
):
    return await HotelService(db).update_hotel_partially(hotel_data=hotel_data, hotel_id=hotel_id)


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id=hotel_id)
    return {"satus": "OK"}
