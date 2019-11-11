from json import JSONDecodeError

import sqlalchemy as sa
from aiohttp import web
from marshmallow import ValidationError
from sqlalchemy import func

from api.models import shelter, pet
from api.serializers import PetSerializer, ShelterSerializer
from api.utils import validate_uuid4


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
            query = self.table.select() \
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


class BaseListView(web.View):
    table = None
    serializer = None

    async def create(self):

        try:
            data = await self.request.json()
        except JSONDecodeError:
            raise web.HTTPBadRequest(body="No data provided")

        try:
            result = self.serializer.load(data)
        except ValidationError as e:
            response = e.messages
            response['error'] = "Validation error"
            return web.json_response(
                response
            )

        async with self.request.app['db'].acquire() as conn:
            await conn.execute(self.table.insert().values(result))

        return result


class PetsView(BaseListView):
    table = pet
    serializer = PetSerializer()

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

            return web.json_response(
                self.serializer.dump(pets, many=True)
            )

    async def post(self):
        result = await self.create()

        return web.json_response(
            {
                "message": "created",
                "pet": self.serializer.dump(result)
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
            result = self.serializer.load(data, partial=True)
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


class SheltersView(BaseListView):
    table = shelter
    serializer = ShelterSerializer()

    async def get(self):
        city = self.request.rel_url.query.get('city', '')

        async with self.request.app['db'].acquire() as conn:
            query = shelter.select()
            # query2 = sa.select([func.count(pet.c.id).label('pets_available'), pet.c.shelter_id])\
            #     .where(pet.c.available == True)\
            #     .group_by('shelter_id')
            # join = shelter.join(query2, query.c.id == query2.c.shelter_id)
            # query = shelter.select().select_from(join)
            if city:
                query = shelter.select() \
                    .where(shelter.c.city == city)

            cursor = await conn.execute(query)
            shelters = await cursor.fetchall()
            # print(shelters)
            # cursor = await conn.execute(query2)
            # q2 = await cursor.fetchall()
            # print(q2)

            return web.json_response(
                self.serializer.dump(shelters, many=True)
            )

    async def post(self):
        result = await self.create()

        return web.json_response(
            {
                "message": "created",
                "shelter": self.serializer.dump(result)
            }
        )


class ShelterDetailView(BaseDetailView):
    table = shelter
    serializer = ShelterSerializer()
    key = "uuid"

    async def get(self):
        instance = await self.get_object()
        return web.json_response(
            self.serializer.dump(instance)
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


class ShelterPetsView(BaseListView):
    table = pet
    serializer = PetSerializer()

    async def get(self):
        shelter_id = self.request.match_info.get("uuid", None)
        pet_type = self.request.rel_url.query.get('type', '')

        async with self.request.app['db'].acquire() as conn:
            query = pet.select() \
                .where(pet.c.shelter_id == shelter_id)
            if pet_type:
                query = pet.select() \
                    .where(pet.c.shelter_id == shelter_id) \
                    .where(pet.c.pet_type == pet_type)

            cursor = await conn.execute(query)
            shelter_pets = await cursor.fetchall()

            return web.json_response(
                self.serializer.dump(shelter_pets, many=True)
            )
