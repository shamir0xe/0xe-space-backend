import logging
from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import APIRouter, FastAPI, HTTPException, Request
from pylib_0xe.database.actions.release_session import ReleaseSession
from pylib_0xe.types.database_types import DatabaseTypes
from src.models.post import Post
from src.repositories.repository import Repository
from src.decorators.auth import auth
from src.models.user import User
from src.types.exception_types import ExceptionTypes
from src.types.user_roles import UserRoles
from src.types.api.masked_post import MaskedPost
from src.actions.blog.calculate_avg_rating import CalculateAvgRating


LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize
    # LOGGER.info(f"in the lifespan of the general router")
    yield
    # cleanup
    # LOGGER.info(f"Cleanup")


router = APIRouter(
    prefix=f"/blog",
    tags=["blog"],
    lifespan=lifespan,
)


@router.post("/create")
@auth(UserRoles.ADMIN)
async def create(
    title: str, content: str, request: Request, user_id: Optional[str] = None
) -> MaskedPost:
    if not user_id:
        raise HTTPException(401, ExceptionTypes.AUTH_REQUIRED.value)
    user, _ = Repository(User).read_by_id(user_id)
    blog, session = Repository(Post).create(
        Post(title=title, content=content, user=user), db_session_keep_alive=True
    )
    rating_avg = CalculateAvgRating(post=blog).calculate()
    ReleaseSession(DatabaseTypes.I, session).release()
    return MaskedPost(**blog.to_dict(), rating_avg=rating_avg)


@router.post("/read")
async def read() -> List[MaskedPost]:
    ## MaskedPost without rating
    blogs, _ = Repository(Post).read()
    return [MaskedPost(**blog.to_dict()) for blog in blogs]


@router.post("/read_by_id/{id}")
async def read_by_id(id: str) -> MaskedPost:
    blog, session = Repository(Post).read_by_id(id, db_session_keep_alive=True)
    rating_avg = CalculateAvgRating(post=blog).calculate()
    ReleaseSession(DatabaseTypes.I, session).release()
    return MaskedPost(**blog.to_dict(), rating_avg=rating_avg)


@router.post("/update/{id}")
@auth(UserRoles.ADMIN)
async def update(
    id: str,
    request: Request,
    title: Optional[str] = None,
    content: Optional[str] = None,
    user_id: Optional[str] = None,
) -> MaskedPost:
    if not user_id:
        raise HTTPException(401, ExceptionTypes.AUTH_REQUIRED.value)
    blog, session = Repository(Post).read_by_id(id, db_session_keep_alive=True)
    if title:
        blog.title = title
    if content:
        blog.content = content
    session.commit()
    rating_avg = CalculateAvgRating(post=blog).calculate()
    ReleaseSession(DatabaseTypes.I, session).release()
    return MaskedPost(**blog.to_dict(), rating_avg=rating_avg)


@router.post("/delete/{id}")
@auth(UserRoles.ADMIN)
async def delete(
    id: str,
    request: Request,
    user_id: Optional[str] = None,
) -> MaskedPost:
    if not user_id:
        raise HTTPException(401, ExceptionTypes.AUTH_REQUIRED.value)
    blog, _ = Repository(Post).read_by_id(id)
    Repository(Post).delete(blog)
    return MaskedPost(**blog.to_dict())
