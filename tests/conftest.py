import pytest

from src.database import Base, engine_null_pull
from src.models import *

@pytest.fixture(scope="session", autouse=True)
async def async_main() -> None:
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)