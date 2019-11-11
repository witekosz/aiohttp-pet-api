import asyncio
import logging

from aiopg.sa import create_engine
from sqlalchemy.sql.ddl import CreateTable

import settings
from api.models import shelter, pet


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


async def init_db(app):
    logging.info("DB Init")
    app['db'] = await get_engine()


async def init_db_data():
    async with get_engine() as engine:
        async with engine.acquire() as conn:
            await conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
            await check_and_create_table(conn, shelter, "shelter")
            await check_and_create_table(conn, pet, "pet")


async def close_db(app):
    app['db'].close()
    await app['db'].wait_closed()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db_data())
