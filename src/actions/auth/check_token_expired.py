from dataclasses import dataclass
from datetime import UTC, datetime
from pylib_0xe.config.config import Config

from src.models.token import Token


@dataclass
class CheckTokenExpired:
    token: Token

    def check(self) -> bool:
        """Check whether the token has been expired or not"""
        if (
            datetime.now(UTC) - self.token.updated_at.replace(tzinfo=UTC)
        ).total_seconds() > Config.read("api.token_timeout"):
            return True

        return False
