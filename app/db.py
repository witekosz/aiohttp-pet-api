import asyncio
from aiopg.sa import create_engine
import sqlalchemy as sa

import settings
from api.models import shelter, pet


db_engine = create_engine(
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
)


def create_tables(engine):
    meta = sa.MetaData()
    meta.create_all(bind=engine, tables=[shelter, pet])


async def init_db(app):
    app['db'] = await db_engine


async def close_db(app):
    app['db'].close()
    await app['db'].wait_closed()


if __name__ == '__main__':
    await create_tables(db_engine)
