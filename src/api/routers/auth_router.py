import logging
import traceback
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import APIRouter, FastAPI, HTTPException, Request
from pylib_0xe.database.actions.release_session import ReleaseSession
from pylib_0xe.database.mediators.engine_mediator import DatabaseTypes

from src.facades.email_facade import EmailFacade
from src.models.verification import Verification
from src.actions.auth.check_token_expired import CheckTokenExpired
from src.facades.password_facade import PasswordFacade
from src.models.token import Token
from src.repositories.user_repository import UserRepository
from src.repositories.repository import Repository
from src.decorators.auth import auth
from src.models.user import User
from src.types.exception_types import ExceptionTypes
from src.types.api.masked_user import MaskedUser
from src.types.email_templates import EmailTemplates
from src.types.verified_by import VerifiedBy
from src.validators.email_validator import EmailValidator
from src.validators.username_validator import UsernameValidator
from src.types.api.server_response import ServerResponse


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
async def login(username: str, password: str) -> str:
    user, session = UserRepository(User).read_by_username(
        username, db_session_keep_alive=True
    )
    if (
        PasswordFacade.verify_password(password, user.password)
        and user.is_email_confirmed
    ):
        if not user.token or CheckTokenExpired(user.token).check():
            user.token = Token()
            session.add(user)
    else:
        ReleaseSession(DatabaseTypes.I, session).release()
        # Modify returning message
        message = "Username and password do not match"
        if not user.is_email_confirmed:
            message = "Need to confirm your email first"
        raise HTTPException(401, message)
    session.commit()
    ReleaseSession(DatabaseTypes.I, session).release()
    return user.token.id


@router.get("/confirm-code")
async def confirm_code(
    username: str, code: str, password: Optional[str] = None
) -> ServerResponse:
    # TODO: imp
    return ServerResponse()


@router.get("/reset-password")
async def reset_password(username: str) -> ServerResponse:
    # TODO: imp
    return ServerResponse()


@router.post("/register")
async def register(
    username: str,
    password: str,
    email: str,
    name: Optional[str] = None,
) -> MaskedUser:
    # Validations
    if not UsernameValidator(username).validate():
        raise HTTPException(400, "Invalid username")
    if not EmailValidator(email).validate():
        raise HTTPException(400, "Invalid email")
    if not password:
        raise HTTPException(400, "Password should not be empty")

    # Uniqueness
    control = True
    try:
        UserRepository(User).read_by_username(username)
        control = False
        raise HTTPException(409, "Username already exists")
    except Exception as e:
        if not control:
            raise e
    try:
        UserRepository(User).read_by_email(email)
        control = False
        raise HTTPException(409, "Email address already exists")
    except Exception as e:
        if not control:
            raise e

    # Create the user
    user, session = Repository(User).create(
        User(
            username=username,
            email=email,
            name=name,
            password=PasswordFacade.hash(password),
            is_admin=False,
            is_email_confirmed=False,
        ),
        db_session_keey_alive=True,
    )

    # Send the verification code
    user.verification = Verification(by=VerifiedBy.EMAIL)
    session.commit()

    try:
        EmailFacade.send(
            email=email,
            template=EmailTemplates.VERIFICATION_CODE,
            code=user.verification.code,
            username=user.username,
            user_id=user.id,
        )
    except:
        ReleaseSession(DatabaseTypes.I, session).release()
        raise HTTPException(500, "Cannot send the email")

    ReleaseSession(DatabaseTypes.I, session).release()
    return MaskedUser(**user.to_dict())


@router.post("/resend-code")
async def resend_code(username: str, email: str) -> MaskedUser:
    session = None
    try:
        user, session = UserRepository(User).read_by_username(
            username, db_session_keep_alive=True
        )
        if user.email != email:
            ReleaseSession(DatabaseTypes.I, session).release()
            raise Exception("Username & password dont match")
    except Exception:
        raise HTTPException(401, "Username and email don't match")

    user.verification = Verification(by=VerifiedBy.EMAIL)
    session.commit()

    # TODO: Add a rate-limit for sending email
    try:
        EmailFacade.send(
            email=email,
            template=EmailTemplates.VERIFICATION_CODE,
            code=user.verification.code,
            username=user.username,
            user_id=user.id,
        )
    except:
        traceback.print_exc()
        ReleaseSession(DatabaseTypes.I, session).release()
        raise HTTPException(500, "Cannot send the email")

    ReleaseSession(DatabaseTypes.I, session).release()
    return MaskedUser(**user.to_dict())


@router.get("/logout")
@auth()
async def logout(request: Request, user_id: Optional[str] = None) -> MaskedUser:
    if not user_id:
        raise HTTPException(401, ExceptionTypes.AUTH_REQUIRED.value)
    user, session = Repository(User).read_by_id(user_id, db_session_keep_alive=True)
    if user.token:
        session.delete(user.token)
        session.commit()
    ReleaseSession(DatabaseTypes.I, session).release()
    return MaskedUser(**user.to_dict())
