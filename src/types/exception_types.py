from enum import Enum


class ExceptionTypes(Enum):
    REQUEST_INVALID = "request_invalid"
    PERMISSION_REQUIRED = "permission_required"
    ALREADY_EXISTS = "already_exists"
    AUTH_REQUIRED = "auth_required"
    TOKEN_INVALID = "token_invalid"
