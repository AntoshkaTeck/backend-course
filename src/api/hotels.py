from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi.openapi.models import Example
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPATCH, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/")
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        date_from: date = Query(example="2025-10-21"),
        date_to: date = Query(example="2025-10-24"),
        title: str | None = Query(default=None, description="Название отеля"),
        location: str | None = Query(default=None, description="Расположение отеля"),
):
    per_page = pagination.per_page or 5

    return await db.hotels.get_filtered_by_date(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )

@router.get("/{hotel_id}", summary="Получить один отель")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("/")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(
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
        ),
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"satus": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.update(hotel_data, id=hotel_id)
    await db.commit()

    return {"satus": "OK"}


@router.patch("/{hotel_id}")
async def update_hotel_part(
        hotel_id: int,
        hotel_data: HotelPATCH,
        db: DBDep,
):
    await db.hotels.update(hotel_data, exclude_unset=True , id=hotel_id)
    await db.commit()

    return {"satus": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"satus": "OK"}
