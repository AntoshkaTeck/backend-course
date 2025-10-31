from src.api.dependencies import get_db_manager
from src.schemas.hotels import HotelAdd


async def test_add_hotel():
    hotel_data = HotelAdd(title="Hotel 1", location="Amsterdam")
    async with get_db_manager(null_pool=True) as db:
        new_hotel_data = await db.hotels.add(hotel_data)
        await db.commit()
