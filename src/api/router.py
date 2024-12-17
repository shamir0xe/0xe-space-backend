import logging
from contextlib import asynccontextmanager

from pylib_0xe.config.config import Config
from fastapi import APIRouter, FastAPI

# from .auth_router import router as auth_router
# from .user_router import router as user_router
from .general_router import router as general_router


version = Config.read("api.version")

LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize
    LOGGER.info(f"in the lifespan of the main router")
    yield
    # cleanup
    LOGGER.info(f"Cleanup")
    # await ClientManager().cleanup()
    # await run_in_threadpool(CleanupSessions.cleanup)


router = APIRouter(
    prefix=f"/v{version}",
    lifespan=lifespan,
    responses={404: {"description": "Not found"}},
)

router.include_router(general_router)
# router.include_router(auth_router)
# router.include_router(user_router)
