import logging

import sqlalchemy as sa
from aiohttp import web
from marshmallow import ValidationError

from api.models import shelter, pet
from api.serializers import PetSerializer, ShelterSerializer
from api.utils import validate_uuid4
from settings import PET_TYPES


async def index(request):
    """Index view"""
    text = "REST SHELTER API"
    return web.Response(text=text)


class BaseDetailView(web.View):
    table = None
    serializer = None
    key = None

    async def get_object(self):
        object_id = self.request.match_info.get(self.key, None)
        validate_id = await validate_uuid4(object_id)

        if not validate_id:
            raise web.HTTPBadRequest(body="Invalid UUID format")

        async with self.request.app['db'].acquire() as conn:
            query = self.table.select()\
                .where(self.table.c.id == validate_id)
            cursor = await conn.execute(query)
            obj = await cursor.first()

            if obj is None:
                raise web.HTTPNotFound(body="Object not found")

            return obj

    async def perform_destroy(self, instance):
        async with self.request.app['db'].acquire() as conn:
            query = sa.delete(self.table) \
                .where(self.table.c.id == instance['id'])
            await conn.execute(query)


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


class PetDetailView(BaseDetailView):
    table = pet
    serializer = PetSerializer()
    key = "uuid"

    async def get(self):
        obj = await self.get_object()
        return web.json_response(
            self.serializer.dump(obj)
        )

    async def patch(self):
        instance = await self.get_object()
        data = await self.request.json()

        try:
            result = self.serializer.load(data)
        except ValidationError as e:
            response = e.messages
            response['error'] = "Validation error"
            return web.json_response(
                response
            )

        async with self.request.app['db'].acquire() as conn:
            await conn.execute(
                pet.update().values(result).where(pet.c.id == instance.id)
            )
        instance_updated = await self.get_object()

        return web.json_response(
            {
                'message': 'updated',
                'pet': self.serializer.dump(instance_updated)
            }
        )

    async def delete(self):
        instance = await self.get_object()
        await self.perform_destroy(instance)
        return web.json_response(
            {
                'message': 'deleted',
                'pet': self.serializer.dump(instance)
            },
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
        data = await self.request.json()

        try:
            shelter_name = data['shelter-name']
            full_address = data['full-address']
            city = data['city']

        except KeyError:
            return web.json_response(
                {
                    'error': 'Send required data(shelter-name, full-address, city)'
                }
            )

        async with self.request.app['db'].acquire() as conn:
            await conn.execute(
                shelter.insert().values(
                    {
                        "shelter_name": shelter_name,
                        "full_address": full_address,
                        "city": city
                    }
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


class ShelterDetailView(BaseDetailView):
    table = shelter
    serializer = ShelterSerializer()
    key = "uuid"

    async def get(self):
        obj = await self.get_object()
        return web.json_response(
            self.serializer.dump(obj)
        )

    async def delete(self):
        instance = await self.get_object()
        await self.perform_destroy(instance)
        return web.json_response(
            {
                'message': 'deleted',
                'shelter': self.serializer.dump(instance)
            },
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
