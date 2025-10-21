from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facility import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/", summary="Получить все удобства")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("/", summary="Добавить удобство")
async def create_facility(
        db: DBDep,
        facility_data: FacilityAdd,
):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"satus": "OK", "data": facility}
