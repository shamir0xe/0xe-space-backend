from typing import List, Optional
from sqlalchemy import Boolean, String, false
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.verification import Verification
from src.models.comment import Comment
from src.models.post import Post
from src.models.rating import Rating
from src.models.decorated_base import DecoratedBase
from src.models.token import Token
from src.models.general import General


class User(DecoratedBase):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, index=True, unique=True)
    email: Mapped[Optional[str]] = mapped_column(
        String, nullable=False, index=True, unique=True
    )
    password: Mapped[bytes]
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, server_default=false())
    is_email_confirmed: Mapped[bool] = mapped_column(Boolean, server_default=false())
    token: Mapped["Token"] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    general_pairs: Mapped[List["General"]] = relationship(
        back_populates="updated_by", cascade="all"
    )
    ratings: Mapped[List["Rating"]] = relationship(
        back_populates="created_by", cascade="all, delete-orphan"
    )
    posts: Mapped[List["Post"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    verification: Mapped["Verification"] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False
    )
