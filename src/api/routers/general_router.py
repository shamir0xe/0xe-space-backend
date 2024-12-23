import logging
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import APIRouter, FastAPI, HTTPException, Request

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
    LOGGER.info(f"in the lifespan of the general router")
    yield
    # cleanup
    LOGGER.info(f"Cleanup")


router = APIRouter(
    prefix=f"/general",
    tags=["general"],
    lifespan=lifespan,
)


@router.get("/get-key")
async def get_value(key: str) -> str:
    pair, _ = GeneralRepository(General).read_by_key(key=key)
    return pair.value


@router.get("/set-key")
@auth(UserRoles.ADMIN)
async def set_value(
    key: str, text: str, request: Request, user_id: Optional[str] = None
) -> str:
    if not user_id:
        raise HTTPException(401, ExceptionTypes.AUTH_REQUIRED.value)
    user, _ = Repository(User).read_by_id(user_id)
    try:
        general, _ = Repository(General).create(
            General(key=key, value=text, updated_by=user)
        )
    except Exception:
        general, _ = GeneralRepository(General).read_by_key(key=key)
    general.value = text
    general.updated_by = user
    general, _ = Repository(General).update(general)
    return general.value
