from typing import Optional
from .exception_types import ExceptionTypes
from pylib_0xe.types.exception_types import ExceptionTypes as Ex0xe


class ServerException(Exception):
    exception_type: ExceptionTypes | Ex0xe
    detail: str

    def __init__(
        self, exception_type: ExceptionTypes | Ex0xe, detail: Optional[str] = None
    ):
        self.exception_type = exception_type
        self.detail = detail or exception_type.value
