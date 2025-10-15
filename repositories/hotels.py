from sqlalchemy import select

from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ):
        query = select(HotelsOrm)
        if location:
            query = query.where(HotelsOrm.location.ilike(f"%{location}%"))
        if title:
            query = query.where(HotelsOrm.title.ilike(f"%{title}%"))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return result.scalars().all()
