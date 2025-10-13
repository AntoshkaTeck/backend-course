from fastapi import Query, APIRouter, Body
from fastapi.openapi.models import Example

from dependencies import PaginationDep
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {
        "id": 1, "title": "Сочи", "name": "sochi"
    },
    {
        "id": 2, "title": "Дубай", "name": "dubai"
    },
    {
        "id": 3, "title": "Москва", "name": "moscow"
    },
    {
        "id": 4, "title": "Питер", "name": "piter"
    },
    {
        "id": 5, "title": "Казань", "name": "kazan"
    },
    {
        "id": 6, "title": "Владивосток", "name": "vladivostok"
    },
    {
        "id": 7, "title": "Петропавловск", "name": "petropavlovsk"
    }
]


@router.get("/")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(default=None, description="Название отеля"),
        title: str | None = Query(default=None, description="Название отеля")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)


    start = pagination.per_page * (pagination.page - 1)
    end = pagination.per_page * pagination.page

    return hotels_[start : end]


@router.post("/")
def create_hotel(
        hotel_data: Hotel = Body(
            openapi_examples={
                "1": Example(
                    summary="Сочи",
                    value={
                        "title": "Отель Сочи 5 звезд",
                        "name": "Отель Сочи"
                    }
                ),
                "2": Example(
                    summary="Дубай",
                    value={
                        "title": "Отель Дубай у фонтана",
                        "name": "Отель Дубай"
                    }
                )
            }
        )
):
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })

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
