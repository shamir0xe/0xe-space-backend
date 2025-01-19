import re
from dataclasses import dataclass
from src.validators.base_validator import BaseValidator


@dataclass
class UsernameValidator(BaseValidator):
    username: str
    REGEX = r"^(?=.{8,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"

    def validate(self) -> bool:
        return True if re.match(UsernameValidator.REGEX, self.username) else False
