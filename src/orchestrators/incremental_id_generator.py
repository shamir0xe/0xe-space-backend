import logging
from pylib_0xe.asynchrone.get_lock import GetLock
from pylib_0xe.decorators.singleton import singleton


LOGGER = logging.getLogger(__name__)


@singleton
class IncrementalIdGenerator:
    def __init__(self, cur_post: int = 0) -> None:
        self.cur_post = cur_post
        LOGGER.info(f"Initialized with current-post={self.cur_post}")

    def gen(self) -> str:
        with GetLock.threading_lock():
            self.cur_post += 1
            return str(self.cur_post)

    @staticmethod
    def generate() -> str:
        return IncrementalIdGenerator().gen()
