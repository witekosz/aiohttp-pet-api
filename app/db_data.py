import asyncio

import settings
from db import get_engine


async def load_sample_data(filename):
    """
    Loads sample data to db from sql queries
    :param filename string e.g. 'data.sql'
    """

    sql = (settings.SQL_DIR / filename).read_text()
    async with get_engine() as engine:
        async with engine.acquire() as conn:
            await conn.execute(sql)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(load_sample_data('data_shelters.sql'))
    loop.run_until_complete(load_sample_data('data_pets.sql'))
