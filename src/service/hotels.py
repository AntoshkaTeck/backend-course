from datetime import date

from src.exceptions import ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import HotelAdd, HotelPatch, Hotel
from src.service.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_date(
        self,
        pagination,
        date_from: date,
        date_to: date,
        title: str | None,
        location: str | None,
    ) -> list[Hotel]:
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_date(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_hotel(self, hotel_id: int) -> Hotel:
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, hotel_data: HotelAdd) -> Hotel:
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def update_hotel(self, hotel_data: HotelAdd, hotel_id: int) -> Hotel:
        hotel = await self.db.hotels.update(hotel_data, id=hotel_id)
        await self.db.commit()
        return hotel

    async def update_hotel_partially(self, hotel_data: HotelPatch, hotel_id: int) -> Hotel:
        hotel = await self.db.hotels.update(hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()
        return hotel

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def get_hotel_and_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex
