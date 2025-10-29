import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import sys
from pathlib import Path

from src.api.dependencies import get_db

sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_connector

from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.auth import router as router_auth
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images


async def send_emails_simple_example():
    async for db in get_db():
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")

async def run_send_emails_scheduler():
    while True:
        await send_emails_simple_example()
        await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # При старте проекта
    await asyncio.create_task(run_send_emails_scheduler())
    await redis_connector.connect()
    FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
    yield
    await redis_connector.close()
    # При выкл/перезагрузке проекта


app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
