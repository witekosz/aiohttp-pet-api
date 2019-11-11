import pytest
from aiohttp import web

from api.routes import setup_routes
from db import close_db, init_db


@pytest.fixture
async def test_app(loop):
    app = web.Application()

    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)

    setup_routes(app)
    return app


@pytest.fixture
async def get_pet_id(aiohttp_client, test_app, loop):
    client = await aiohttp_client(test_app)

    resp = await client.get('/pets')
    data = await resp.json()

    return data[0]['id']
