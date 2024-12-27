from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.decorated_base import DecoratedBase
from src.models.rating import Rating

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.post import Post


class Comment(DecoratedBase):
    __tablename__ = "comments"

    content: Mapped[str]
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="comments")
    post_id: Mapped[str] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")

    ratings: Mapped[List["Rating"]] = relationship(
        primaryjoin="and_(Rating.ratingable_type=='comment', foreign(Rating.ratingable_id)==Comment.id)",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
