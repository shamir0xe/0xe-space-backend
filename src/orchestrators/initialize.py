from pylib_0xe.database.mediators.engine_mediator import EngineMediator
from pylib_0xe.types.database_types import DatabaseTypes

from src.models.post import Post
from src.orchestrators.incremental_id_generator import IncrementalIdGenerator
from src.repositories.repository import Repository
from src.database.database_engine import DatabaseEngine
from src.actions.database.run_seeders import RunSeeders


class Initialize:
    def __init__(self) -> None:
        EngineMediator().register(DatabaseTypes.I, DatabaseEngine().engine)
        RunSeeders.run()

        # Incremental ID Generator
        posts = Repository(Post).read()[0]
        last_one = 0
        for post in posts:
            last_one = last_one if last_one > int(post.id) else int(post.id)
        IncrementalIdGenerator(cur_post=last_one)
