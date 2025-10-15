from fastapi import Query, APIRouter, Body
from fastapi.openapi.models import Example

from sqlalchemy import insert, select

from repositories.hotels import HotelsRepository
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.schemas.hotels import Hotel, HotelPATCH
from src.models.hotels import HotelsOrm

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(default=None, description="Название отеля"),
        location: str | None = Query(default=None, description="Расположение отеля"),
):
    per_page = pagination.per_page or 5
    async with (async_session_maker() as session):
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.post("/")
async def create_hotel(
        hotel_data: Hotel = Body(
            openapi_examples={
                "1": Example(
                    summary="Сочи",
                    value={
                        "title": "Отель Сочи 5 звезд",
                        "location": "ул. Моря 1"
                    }
                ),
                "2": Example(
                    summary="Дубай",
                    value={
                        "title": "Отель Дубай у фонтана",
                        "location": "ул. Шейха 2"
                    }
                )
            }
        )
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data.model_dump())
        await session.commit()

    return {"satus": "OK", "data": hotel}


@router.put("/{hotel_id}")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name

    return {"satus": "OK"}


@router.patch("/{hotel_id}")
def update_hotel_part(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title if hotel_data.title else hotel["title"]
            hotel["name"] = hotel_data.name if hotel_data.name else hotel["name"]

    return {"satus": "OK"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]

    return {"satus": "OK"}
