import logging
from datetime import datetime

from psycopg2.errors import lookup as psg_error
import sqlalchemy as sa
from aiohttp import web

from api.models import shelter, pet
from db import check_and_create_table
from settings import PET_TYPES


async def index(request):
    """Index view"""
    text = "REST SHELTER API"
    async with request.app['db'].acquire() as conn:
        await conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
        await check_and_create_table(conn, shelter, "shelter")
        await check_and_create_table(conn, pet, "pet")

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

    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            query = shelter.select()
            cursor = await conn.execute(query)
            shelters = await cursor.fetchall()
            data = [str(s) for s in shelters]

            return web.json_response(data)

    async def post(self):
        data = await self.request.post()
        try:
            shelter_name = data['shelter-name']
            full_address = data['full-address']
            city = data['city']

        except KeyError:
            return web.json_response(
                {
                    'error': 'Send required post form data(shelter-name, full-address, city)'
                }
            )

        async with self.request.app['db'].acquire() as conn:
            await conn.execute(
                shelter.insert().values(
                    shelter_name=shelter_name,
                    full_address=full_address,
                    city=city
                )
            )

        return web.json_response(
            {
                "message": "ok",
                "shelter": {
                    "shelter_name": shelter_name,
                    "full_address": full_address,
                    "city": city
                }
            }
        )


class ShelterDetailView(web.View):

    async def get(self):
        shelter_id = self.request.match_info.get("uuid", None)
        async with self.request.app['db'].acquire() as conn:
            query = shelter.select()\
                .where(shelter.c.id == shelter_id)
            try:
                cursor = await conn.execute(query)
                shelters = await cursor.fetchall()
                data = [str(s) for s in shelters]

                return web.json_response(data)

            except psg_error("22P02"):  # InvalidTextRepresentation
                return web.json_response(
                    {
                        'error': 'Invalid UUID format'
                    }
                )

    async def delete(self):
        shelter_id = self.request.match_info.get("uuid", None)
        async with self.request.app['db'].acquire() as conn:
            query = sa.delete(shelter)\
                .where(shelter.c.id == shelter_id)
            try:
                await conn.execute(query)
                return web.json_response(
                    {
                        'message': 'Deleted'
                    }
                )

            except psg_error("22P02"):  # InvalidTextRepresentation
                return web.json_response(
                    {
                        'error': 'Invalid UUID format'
                    }
                )


class ShelterPetsView(web.View):

    async def get(self):
        shelter_id = self.request.match_info.get("uuid", None)

        try:
            pet_type = self.request.rel_url.query['type']
        except KeyError:
            return web.json_response(
                {
                    'error': 'Send required query params(type)'
                }
            )

        if pet_type not in PET_TYPES:
            return web.json_response(
                {
                    'error': 'Unknown pet type'
                }
            )

        async with self.request.app['db'].acquire() as conn:
            query = pet.select()\
                .where(pet.c.shelter_id == shelter_id)\
                .where(pet.c.pet_type == pet_type)
            cursor = await conn.execute(query)
            shelter_pets = await cursor.fetchall()
            data = [str(s) for s in shelter_pets]

            return web.json_response(data)
