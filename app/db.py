import asyncio
from aiopg.sa import create_engine
import sqlalchemy as sa

import settings
from api.models import shelter, pet


def get_engine():
    engine = create_engine(
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        isolation_level='AUTOCOMMIT'
    )
    return engine


def create_tables():
    meta = sa.MetaData()
    meta.create_all(bind=get_engine(), tables=[shelter, pet])


# async def init_db(app):
#     app['db'] = await db_engine


async def close_db(app):
    app['db'].close()
    await app['db'].wait_closed()


if __name__ == '__main__':
    create_tables()
