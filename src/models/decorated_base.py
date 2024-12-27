from typing import Dict, Set
from pylib_0xe.string.generate_id import GenerateId
from pylib_0xe.utils.time.get_current_time import GetCurrentTime
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from datetime import datetime
from src.orchestrators.incremental_id_generator import IncrementalIdGenerator


class DecoratedBase(DeclarativeBase):
    __abstract__ = True
    use_incremental_id: bool = False

    updated_at: Mapped[datetime] = mapped_column(
        index=True,
        doc="Last Update Time",
        default=GetCurrentTime.get,
        onupdate=GetCurrentTime.get,
    )
    created_at: Mapped[datetime] = mapped_column(
        index=True, doc="Creation Time", default=GetCurrentTime.get
    )

    @declared_attr
    def id(cls) -> Mapped[str]:
        if getattr(cls, "use_incremental_id", False):
            return mapped_column(
                String,
                primary_key=True,
                default=IncrementalIdGenerator.generate,
            )
        else:
            return mapped_column(String, primary_key=True, default=GenerateId.generate)

    def to_dict(self, exclude: Set[str] = set()) -> Dict:
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if column.name not in exclude
        }
