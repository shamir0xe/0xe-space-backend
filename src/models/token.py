from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.decorated_base import DecoratedBase

if TYPE_CHECKING:
    from .user import User


class Token(DecoratedBase):
    __tablename__ = "tokens"

    user: Mapped["User"] = relationship(
        back_populates="token", single_parent=True, uselist=False
    )
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE")
    )
