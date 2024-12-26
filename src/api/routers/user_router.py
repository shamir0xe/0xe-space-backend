import logging
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import APIRouter, FastAPI, HTTPException, Request
from src.repositories.repository import Repository
from src.decorators.auth import auth
from src.models.user import User
from src.types.exception_types import ExceptionTypes
from src.types.api.masked_user import MaskedUser


LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize
    # LOGGER.info(f"in the lifespan of the general router")
    yield
    # cleanup
    # LOGGER.info(f"Cleanup")


router = APIRouter(
    prefix=f"/user",
    tags=["user"],
    lifespan=lifespan,
)


@router.post("/info")
@auth()
async def user_info(request: Request, user_id: Optional[str] = None) -> MaskedUser:
    if not user_id:
        raise HTTPException(401, ExceptionTypes.AUTH_REQUIRED.value)
    user, _ = Repository(User).read_by_id(user_id)
    return MaskedUser(**user.to_dict())
