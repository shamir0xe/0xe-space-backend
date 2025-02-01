from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.decorated_base import DecoratedBase
from src.models.rating import Rating
from src.models.comment import Comment

if TYPE_CHECKING:
    from src.models.user import User


class Post(DecoratedBase):
    __tablename__ = "posts"
    use_incremental_id = True

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    title: Mapped[str]
    content: Mapped[str]
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="post", cascade="all, delete-orphan"
    )

    ratings: Mapped[List["Rating"]] = relationship(
        primaryjoin="and_(Post.id==foreign(Rating.ratingable_id), Rating.ratingable_type=='post')",
        lazy="dynamic",
        cascade="all, delete-orphan",
        overlaps="comment,ratings,post",
    )
