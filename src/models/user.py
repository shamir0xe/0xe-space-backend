from typing import List, Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.decorated_base import DecoratedBase
from src.models.token import Token
from src.models.general import General


class User(DecoratedBase):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, index=True, unique=True)
    password: Mapped[str] = mapped_column(String(64))
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_admin: Mapped[bool] = mapped_column(String, default=False)
    token: Mapped["Token"] = relationship(
        back_populates="user", cascade="all", uselist=False
    )
    general_pairs: Mapped[List["General"]] = relationship(
        back_populates="updated_by", cascade="all"
    )
