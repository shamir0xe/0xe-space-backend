import logging
from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI
from pylib_0xe.config.config import Config

from src.orchestrators.initialize import Initialize
from .routers.auth_router import router as auth_router
from .routers.general_router import router as general_router
from .routers.user_router import router as user_router
from .routers.blog_router import router as blog_router


version = Config.read("api.version")

LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize
    LOGGER.info(f"in the lifespan of the main router")
    Initialize()
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
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(blog_router)
