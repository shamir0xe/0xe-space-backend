import logging
from sqlalchemy import Engine, create_engine

from pylib_0xe.database.infos.postgres_database_info import PostgresDatabaseInfo
from pylib_0xe.decorators.singleton import singleton
from pylib_0xe.config.config import Config
from ..models.decorated_base import DecoratedBase

LOGGER = logging.getLogger("[ENGINE]")


@singleton
class DatabaseEngine:
    engine: Engine

    def __init__(self) -> None:
        postgres_data = PostgresDatabaseInfo(**Config.read_env("db.postgres"))
        LOGGER.info(f"pg-data: {postgres_data}")
        self.engine = create_engine(
            url="postgresql+psycopg://{}:{}@{}:{}/{}".format(
                postgres_data.user,
                postgres_data.password,
                postgres_data.host,
                postgres_data.port,
                postgres_data.db,
            ),
            echo=False,
            pool_pre_ping=True,
        )
        DecoratedBase.metadata.create_all(self.engine)
