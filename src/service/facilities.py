from src.schemas.facilities import FacilityAdd, Facility
from src.service.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def get_all(self):
        return await self.db.facilities.get_all()

    async def create_facility(self, facility_data: FacilityAdd) -> Facility:
        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()

        test_task.delay()  # type: ignore[attr-defined]
        return facility
