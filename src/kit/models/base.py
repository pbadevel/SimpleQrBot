import re
from datetime import datetime

from sqlalchemy import DateTime, inspect
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from src.kit.utils import utc_now


class Model(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


class TimestampedModel(Model):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False, index=True
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=utc_now,
        nullable=True,
        default=None,
        index=True,
    )

    def set_updated_at(self) -> None:
        self.updated_at = utc_now()


class RecordModel(TimestampedModel):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """(camelCase -> snake_case) + optinal 's'"""

        name = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

        if name.endswith("s"):
            return name

        return name + "s"

    def __repr__(self) -> str:
        insp = inspect(self)
        if insp.identity is not None:
            id_value = insp.identity[0]
            return f"{self.__class__.__name__}(id={id_value!r})"
        return f"{self.__class__.__name__}(id=None)"
