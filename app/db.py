import asyncio
import logging
import os

from aiopg.sa import create_engine
import sqlalchemy as sa
from sqlalchemy.sql.ddl import CreateTable

import settings
from api.models import shelter, pet

SQL_DIR = os.path.join(settings.BASE_DIR, 'app', 'sql')

def get_engine():
    engine = create_engine(
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
    )
    return engine


async def check_and_create_table(conn, table, table_name):
    """Check if table exist and creates it if none"""
    sql = f"SELECT to_regclass('public.{table_name}')"
    check_sql = await conn.execute(sql)
    check = await check_sql.fetchone()
    if check[0] is None:
        logging.info(f"Creating table {table_name}")
        await conn.execute(CreateTable(table))


def create_tables(engine):
    meta = sa.MetaData()
    meta.create_all(bind=engine, tables=[shelter, pet])


def drop_tables(engine):
    meta = sa.MetaData()
    meta.drop_all(bind=engine, tables=[shelter, pet])


async def init_db(app):
    logging.info("DB Init")
    app['db'] = await get_engine()


async def sample_data():
    sql_shelters = (settings.BASE_DIR / 'app/sql/shelters_data.sql').read_text()
    sql_pets = (settings.BASE_DIR / 'app/sql/pets_data.sql').read_text()
    async with get_engine() as engine:
        async with engine.acquire() as conn:
            await conn.execute(sql_shelters)
            await conn.execute(sql_pets)


async def close_db(app):
    app['db'].close()
    await app['db'].wait_closed()


if __name__ == '__main__':
    # create_tables(db_engine)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sample_data())
