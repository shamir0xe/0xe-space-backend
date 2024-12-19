from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.decorated_base import DecoratedBase

if TYPE_CHECKING:
    from .user import User


class General(DecoratedBase):
    __tablename__ = "generals"

    key: Mapped[str] = mapped_column(String, index=True, unique=True)
    value: Mapped[str]
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE")
    )
    updated_by: Mapped["User"] = relationship(
        back_populates="general_pairs", single_parent=True
    )
