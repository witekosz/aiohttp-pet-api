import logging

from aiohttp import web

from api.routes import setup_routes
from db import init_db, close_db


def main():
    """Main app loop"""
    logging.basicConfig(level=logging.DEBUG)

    app = web.Application()

    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)

    setup_routes(app)

    web.run_app(app)


if __name__ == '__main__':
    main()
