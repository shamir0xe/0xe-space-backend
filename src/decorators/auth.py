import logging
import functools
from typing import Callable

from fastapi import HTTPException, Request
from src.actions.auth.check_role_permission import CheckRolePermission
from src.facades.authentication import Authentication
from src.types.exception_types import ExceptionTypes
from src.types.user_roles import UserRoles

LOGGER = logging.getLogger(__name__)


def auth(role: UserRoles = UserRoles.REGULAR) -> Callable:
    def decorator_wrapper(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            LOGGER.info("in the auth decorator")
            if "request" not in kwargs:
                raise Exception(ExceptionTypes.REQUEST_INVALID)
            request = kwargs["request"]
            assert isinstance(request, Request)

            user = Authentication().get_user(request=request)
            if not CheckRolePermission.check(user=user, role=role):
                raise HTTPException(403, ExceptionTypes.PERMISSION_REQUIRED.value)
            kwargs["user_id"] = user.id

            result = await func(*args, **kwargs)
            return result

        return wrapper

    return decorator_wrapper
