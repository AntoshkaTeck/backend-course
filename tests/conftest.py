import json
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest

from httpx import ASGITransport, AsyncClient

from src.api.dependencies import get_db_manager, get_db
from src.config import settings
from src.database import Base, engine_null_pull
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pull():
    async with get_db_manager(null_pool=True) as db:
        yield db


@pytest.fixture()
async def db():
    async for db in get_db_null_pull():
        yield db


app.dependency_overrides[get_db] = get_db_null_pull # type: ignore[attr-defined]


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode) -> None:
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def add_data_to_database(setup_database):
    with (
        open("tests/mock_hotels.json", "r") as hotels_file,
        open("tests/mock_rooms.json", "r") as rooms_file
    ):
        hotels_data = json.load(hotels_file)
        rooms_data = json.load(rooms_file)
        async with get_db_manager(null_pool=True) as db_:
            await db_.hotels.add_bulk([HotelAdd.model_validate(h_data) for h_data in hotels_data])
            await db_.rooms.add_bulk([RoomAdd.model_validate(r_data) for r_data in rooms_data])
            await db_.commit()


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
    user_data = {
        "email": "anton.tihov.94@gmail.com",
        "password": "qwerty12345678"
    }

    await ac.post("/auth/register", json=user_data)
