import logging
from contextlib import asynccontextmanager
from typing import Optional

from pylib_0xe.config.config import Config
from fastapi import APIRouter, FastAPI, Request

from decorators.auth import auth
from models.user import User
from types.user_roles import UserRoles


version = Config.read("api.version")

LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize
    LOGGER.info(f"in the lifespan of the general router")
    yield
    # cleanup
    LOGGER.info(f"Cleanup")


router = APIRouter(
    prefix=f"/general",
    tags=["general"],
    lifespan=lifespan,
)


@router.post("/get-about-me")
async def get_value(key: str) -> str:
    pair = GeneralRepository(General).read_by_key(key=key)
    return pair.value


@router.post("/set-about-me")
@auth(UserRoles.ADMIN)
async def set_value(
    key: str, text: str, request: Request, user: Optional[User] = None
) -> str:
    general = Repository(General).create(key=key, value=text)
    return general.value
