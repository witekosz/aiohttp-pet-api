from urllib.parse import urlparse

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    See https://pydantic-docs.helpmanual.io/#settings for details on using and overriding this
    """
    name = 'app2'
    pg_dsn = 'postgres://postgres@localhost:5432/demo_app'
    auth_key = 'bKrJlL4_3CCezDHy6otew6IJ5GvR1Kq3HXA0gRupPYU='
    cookie_name = 'app2'

    @property
    def _pg_dsn_parsed(self):
        return urlparse(self.pg_dsn)

    @property
    def pg_name(self):
        return self._pg_dsn_parsed.path.lstrip('/')
