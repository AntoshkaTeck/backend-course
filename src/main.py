from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.api.exception_handlers import register_exception_handlers
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.auth import router as router_auth
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images
from src.init import redis_connector


@asynccontextmanager
async def lifespan(_: FastAPI):
    # При старте проекта
    await redis_connector.connect()
    FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
    logging.info("FastAPI Cache initialized")
    yield
    await redis_connector.close()
    # При выкл/перезагрузке проекта


app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)
