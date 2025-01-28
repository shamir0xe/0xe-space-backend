from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.decorated_base import DecoratedBase
from src.types.verified_by import VerifiedBy
from random import randint

if TYPE_CHECKING:
    from src.models.user import User


class Verification(DecoratedBase):
    __tablename__ = "verifications"

    code: Mapped[str] = mapped_column(default=lambda: str(randint(10000, 99999)))
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE")
    )
    user: Mapped["User"] = relationship(
        back_populates="verification",
        single_parent=True,
        uselist=False,
    )
    by: Mapped[VerifiedBy]
    try_count: Mapped[int] = mapped_column(default=0)
