import logging

import sqlalchemy as sa
from aiohttp import web
from sqlalchemy.sql.ddl import CreateTable

from api.models import shelter, pet
from db import check_and_create_table


async def index(request):
    """Index view"""
    text = "REST SHELTER API"
    async with request.app['db'].acquire() as conn:
        await conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
        await check_and_create_table(conn, shelter, "shelter")
        await check_and_create_table(conn, pet, "pet")

        logging.info("Test")
        # cursor = await conn.execute(db.question.select())
        # records = await cursor.fetchall()
        # questions = [dict(q) for q in records]
        # return {"questions": questions}
        return web.Response(text=text)


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = f"Hello, {name}"
    return web.Response(text=text)


async def test(request):
    data = {'some': 'data'}
    return web.json_response(data)
