import asyncio

import pytest
from httpx import AsyncClient
from tortoise import Tortoise

from app.api.models import Cargo, TarifDate
from app.main import app
from app.settings import TEST_DATABASE_URL, TORTOISE_ORM


TORTOISE_ORM["connections"]["default"] = TEST_DATABASE_URL


async def init_db() -> None:
    """Initial database connection"""
    await Tortoise.init(
        config=TORTOISE_ORM,
        _create_db=True,
    )
    await Tortoise.generate_schemas()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init_db()
    yield
    await Tortoise._drop_databases()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


async def get_cargo(id: int) -> Cargo | None:
    cargo = await Cargo.get_or_none(id=id)
    return cargo


async def get_count_cargos() -> int:
    count = await Cargo.all().count()
    return count


async def get_count_tarifs() -> int:
    count = await TarifDate().all().count()
    return count
