import asyncio
import logging
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


def drop_tables(engine):
    meta = sa.MetaData()
    meta.drop_all(bind=engine, tables=[shelter, pet])


async def init_db(app):
    logging.info("DB Init")
    app['db'] = await db_engine
    print(app['db'])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(shelter.insert(), [
        {'question_text': 'What\'s new?',
         'pub_date': '2015-12-15 17:17:49.629+02'}
    ])
    conn.execute(pet.insert(), [
        {'choice_text': 'Not much', 'votes': 0, 'question_id': 1},
        {'choice_text': 'The sky', 'votes': 0, 'question_id': 1},
        {'choice_text': 'Just hacking again', 'votes': 0, 'question_id': 1},
    ])
    conn.close()


async def close_db(app):
    app['db'].close()
    await app['db'].wait_closed()


# if __name__ == '__main__':
    # create_tables(db_engine)
    # sample_data(db_engine)
