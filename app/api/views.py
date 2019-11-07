import logging
from datetime import datetime

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


async def pets_view(request):
    """Index view"""
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(pet.select())
        pets = await cursor.fetchall()
        data = [str(p) for p in pets]
        return web.json_response(data)


async def shelters_view(request):
    """Index view"""
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(shelter.select())
        shelters = await cursor.fetchall()
        data = [str(s) for s in shelters]
        return web.json_response(data)


class PetsView(web.View):

    async def get(self):
        token = datetime.now().strftime("%Y%m%d%H%M%S")
        room = self.request.match_info.get("room", None)
        return web.json_response({"room": room, "token": token, "result": "OK"})

    async def post(self):
        room = self.request.match_info.get("room", None)
        token = datetime.now().strftime("%Y%m%d%H%M%S")
        return web.json_response({"room": room, "token": token, "result": "OK"})


class PetDetailView(web.View):

    async def get(self):
        token = datetime.now().strftime("%Y%m%d%H%M%S")
        room = self.request.match_info.get("room", None)
        return web.json_response({"room": room, "token": token, "result": "OK"})

    async def post(self):
        room = self.request.match_info.get("room", None)
        token = datetime.now().strftime("%Y%m%d%H%M%S")
        return web.json_response({"room": room, "token": token, "result": "OK"})


class SheltersView(web.View):

    async def post(self):
        room = self.request.match_info.get("room", None)
        token = datetime.now().strftime("%Y%m%d%H%M%S")
        return web.json_response({"room": room, "token": token, "result": "OK"})


class ShelterDetailView(web.View):

    async def get(self):
        shelter_id = self.request.match_info.get("uuid", None)
        return web.json_response({"shelter": shelter_id})

    async def post(self):
        shelter_id = self.request.match_info.get("uuid", None)
        return web.json_response({"shelter": shelter_id})


class ShelterPetsView(web.View):

    async def get(self):
        shelter_id = self.request.match_info.get("uuid", None)
        return web.json_response({"shelter": shelter_id})


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = f"Hello, {name}"
    return web.Response(text=text)


async def test(request):
    data = {'some': 'data'}
    return web.json_response(data)
