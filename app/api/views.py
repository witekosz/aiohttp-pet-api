import logging
from datetime import datetime

from psycopg2.errors import lookup as psg_error
import sqlalchemy as sa
from aiohttp import web

from api.models import shelter, pet
from api.serializers import PetSerializer, ShelterSerializer
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


class PetsView(web.View):

    async def get(self):
        pet_type = self.request.rel_url.query.get('type', '')
        shelter_id = self.request.rel_url.query.get('shelterid', '')

        async with self.request.app['db'].acquire() as conn:
            query = pet.select()
            if pet_type:
                query = query.where(pet.c.pet_type == pet_type)
            elif shelter_id:
                query = query.where(pet.c.shelter_id == shelter_id)

            cursor = await conn.execute(query)
            pets = await cursor.fetchall()
            schema = PetSerializer()

            return web.json_response(
                schema.dump(pets, many=True)
            )

    async def post(self):
        data = await self.request.post()
        try:
            pet_name = data['pet-name']
            pet_type = data['pet-type']
            desc = data['description']
            shelter_id = data['shelter-id']

        except KeyError:
            return web.json_response(
                {
                    'error': 'Send required post form data(shelter-name, full-address, city)'
                }
            )

        async with self.request.app['db'].acquire() as conn:
            await conn.execute(
                shelter.insert().values(
                    pet_name=pet_name,
                    pet_type=pet_type,
                    desc=desc,
                    shelter_id=shelter_id,
                )
            )

        return web.json_response(
            {
                "message": "ok",
                "shelter": {
                    "pet_name": pet_name,
                    "pet_type": pet_type,
                    "desc": desc,
                    "shelter_id": shelter_id,
                }
            }
        )


class PetDetailView(web.View):

    async def get(self):
        pet_id = self.request.match_info.get("uuid", None)
        async with self.request.app['db'].acquire() as conn:
            query = pet.select()\
                .where(pet.c.id == pet_id)
            try:
                cursor = await conn.execute(query)
                pets = await cursor.fetchall()
                serializer = PetSerializer()

                return web.json_response(
                    serializer.dump(pets, many=True)
                )

            except psg_error("22P02"):  # InvalidTextRepresentation
                return web.json_response(
                    {
                        'error': 'Invalid UUID format'
                    }
                )

    async def patch(self):
        # TODO
        return web.json_response({})

    async def delete(self):
        pet_id = self.request.match_info.get("uuid", None)
        async with self.request.app['db'].acquire() as conn:
            query = sa.delete(pet)\
                .where(pet.c.id == pet_id)
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


class SheltersView(web.View):

    async def get(self):
        city = self.request.rel_url.query.get('city', '')

        async with self.request.app['db'].acquire() as conn:
            if city:
                query = shelter.select()\
                    .where(shelter.c.city == city)
            else:
                query = shelter.select()

            cursor = await conn.execute(query)
            shelters = await cursor.fetchall()
            serializer = ShelterSerializer()

            return web.json_response(
                serializer.dump(shelters, many=True)
            )

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
                serializer = ShelterSerializer()

                return web.json_response(
                    serializer.dump(shelters, many=True)
                )

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
            serializer = PetSerializer()

            return web.json_response(
                serializer.dump(shelter_pets, many=True)
            )
