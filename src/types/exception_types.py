from enum import Enum


class ExceptionTypes(Enum):
    REQUEST_INVALID = "request_invalid"
    PERMISSION_REQUIRED = "permission_required"
    ALREADY_EXISTS = "already_exists"
    AUTH_REQUIRED = "auth_required"
    TOKEN_INVALID = "token_invalid"
    USERNAME_NOT_FOUND = "username_not_found"
    EMAIL_NOT_FOUND = "email_not_found"
    AUTH_HEADER_INVALID = "auth_header_invalid"
