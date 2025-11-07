from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd, Facility
from src.service.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/", summary="Получить все удобства", response_model=list[Facility])
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_all()


@router.post("/", summary="Добавить удобство")
async def create_facility(
    db: DBDep,
    facility_data: FacilityAdd,
):
    return await FacilityService(db).create_facility(facility_data=facility_data)
