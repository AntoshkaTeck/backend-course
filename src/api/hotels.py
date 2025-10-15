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
        return await HotelsRepository(session).get_all()
        # offset = per_page * (pagination.page - 1)
        # limit = per_page
        #
        # query = select(HotelsOrm)
        # if location:
        #     query = query.where(HotelsOrm.location.ilike(f"%{location}%"))
        # if title:
        #     query = query.where(HotelsOrm.title.ilike(f"%{title}%"))
        #
        # query = (
        #     query
        #     .limit(limit).
        #     offset(offset)
        # )
        #
        #
        # result = await session.execute(query)
        # hotels = result.scalars().all()
        #
        # return hotels


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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"satus": "OK"}


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
