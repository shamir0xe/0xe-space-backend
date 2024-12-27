import logging
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM
from src.models.decorated_base import DecoratedBase
from src.types.ratingable_types import RatingableTypes

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.post import Post
    from src.models.comment import Comment

LOGGER = logging.getLogger(__name__)


class Rating(DecoratedBase):
    __tablename__ = "ratings"

    value: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    created_by: Mapped["User"] = relationship(back_populates="ratings")

    # Polymorphic target type
    ratingable_id: Mapped[str] = mapped_column(String, nullable=False)
    ratingable_type: Mapped[RatingableTypes] = mapped_column(
        ENUM("post", "comment", name="ratingable_types"), nullable=False
    )

    post: Mapped["Post"] = relationship(
        "Post",
        primaryjoin="and_(Rating.ratingable_type=='post', foreign(Rating.ratingable_id)==Post.id)",
        uselist=False,
    )
    comment: Mapped["Comment"] = relationship(
        "Comment",
        primaryjoin="and_(Rating.ratingable_type=='comment', foreign(Rating.ratingable_id)==Comment.id)",
        uselist=False,
    )
