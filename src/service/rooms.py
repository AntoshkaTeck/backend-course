from datetime import date

from src.exceptions import ObjectNotFoundException, RoomNotFoundException
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch, Room
from src.service.base import BaseService
from src.service.hotels import HotelService


class RoomService(BaseService):
    async def get_filtered_by_date(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        return await self.db.rooms.get_filtered_by_date(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room(self, room_id: int, hotel_id: int) -> Room:
        return await self.get_room_and_check(hotel_id=hotel_id, room_id=room_id)

    async def create_room(self, hotel_id: int, room_data: RoomAddRequest) -> Room:
        await HotelService(self.db).get_hotel_and_check(hotel_id=hotel_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(_room_data)
        rooms_facilities_data = [
            RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()
        return room

    async def update_room(self, hotel_id: int, room_id: int, room_data: RoomAddRequest) -> Room:
        await self.get_room_and_check(hotel_id=hotel_id, room_id=room_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.update(_room_data, id=room_id, hotel_id=hotel_id)
        await self.db.rooms_facilities.set_rooms_facilities(
            room_id=room_id, facilities_ids=room_data.facilities_ids
        )
        await self.db.commit()
        return room

    async def update_room_partially(
        self, hotel_id: int, room_id: int, room_data: RoomPatchRequest
    ) -> Room:
        await self.get_room_and_check(hotel_id=hotel_id, room_id=room_id)
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
        room = await self.db.rooms.update(
            room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
        )
        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_rooms_facilities(
                room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
            )
        await self.db.commit()
        return room

    async def delete_room(self, hotel_id: int, room_id: int) -> None:
        await self.get_room_and_check(hotel_id=hotel_id, room_id=room_id)
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()

    async def get_room_and_check(self, room_id: int, hotel_id: int | None = None) -> Room:
        try:
            params = {"id": room_id}
            if hotel_id:
                params["hotel_id"] = hotel_id
            return await self.db.rooms.get_one(**params)
        except ObjectNotFoundException:
            raise RoomNotFoundException
