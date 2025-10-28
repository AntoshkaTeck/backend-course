import json

from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.init import redis_connector
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/", summary="Получить все удобства")
async def get_facilities(db: DBDep):
    cache_facilities = await redis_connector.get("facilities")
    if not cache_facilities:
        facilities =  await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        await redis_connector.set("facilities", json.dumps(facilities_schemas), 10)
        return facilities
    else:
        return json.loads(cache_facilities)


@router.post("/", summary="Добавить удобство")
async def create_facility(
        db: DBDep,
        facility_data: FacilityAdd,
):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"satus": "OK", "data": facility}
