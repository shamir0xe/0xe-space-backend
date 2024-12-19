import logging
from contextlib import asynccontextmanager
from typing import Optional
from pylib_0xe.config.config import Config
from fastapi import APIRouter, FastAPI, Request

from src.repositories.general_repository import GeneralRepository
from src.repositories.repository import Repository
from src.decorators.auth import auth
from src.models.general import General
from src.models.user import User
from src.types.user_roles import UserRoles
from src.types.exception_types import ExceptionTypes


LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize
    # LOGGER.info(f"in the lifespan of the general router")
    yield
    # cleanup
    # LOGGER.info(f"Cleanup")


router = APIRouter(
    prefix=f"/auth",
    tags=["auth"],
    lifespan=lifespan,
)


@router.post("/login")
async def login(user_name: str, password: str) -> str:
    # TODO:
    return ""


@router.get("/logout")
@auth
async def logout(request: Request, user: Optional[User] = None) -> str:
    if not user:
        raise Exception(ExceptionTypes.AUTH_REQUIRED)
    # TODO:
    return ""
