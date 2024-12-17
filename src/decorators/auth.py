import functools
from typing import Callable

from fastapi import Request
from src.actions.auth.check_role_permission import CheckRolePermission
from src.facades.authentication import Authentication
from src.types.exception_types import ExceptionTypes
from src.types.user_roles import UserRoles


def auth(_func=None, *, role: UserRoles = UserRoles.REGULAR) -> Callable:
    def decorator_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if "request" not in kwargs:
                raise Exception(ExceptionTypes.REQUEST_INVALID)
            request = kwargs["request"]
            assert isinstance(request, Request)

            user = Authentication().get_user(request=request)
            if not CheckRolePermission.check(user=user, role=role):
                raise Exception(ExceptionTypes.PERMISSION_REQUIRED)
            kwargs["user"] = user

            result = func(*args, **kwargs)
            return result

        return wrapper

    if _func is None:
        return decorator_wrapper
    return decorator_wrapper(_func)
