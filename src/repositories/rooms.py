from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.exceptions import validate_booking_dates, ObjectNotFoundException
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.mappers.mappers import RoomDataMapper, RoomWithRelsDataMapper
from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_date(self, hotel_id: int, date_from: date, date_to: date):
        validate_booking_dates(date_to=date_to, date_from=date_from)

        rooms_ids_to_get = rooms_ids_for_booking(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

        query = (
            select(self.model)
            .options(
                selectinload(self.model.facilities),
            )
            .where(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        rooms = result.scalars().all()
        return [RoomWithRelsDataMapper.map_to_domain_entity(model) for model in rooms]

    async def get_one_with_rels(self, **filter_by):
        query = (
            select(self.model)
            .options(
                selectinload(self.model.facilities),
            )
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
            return RoomWithRelsDataMapper.map_to_domain_entity(model)
        except NoResultFound:
            raise ObjectNotFoundException
