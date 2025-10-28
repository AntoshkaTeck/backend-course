import json

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.init import redis_connector
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/", summary="Получить все удобства")
@cache(expire=10)
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
