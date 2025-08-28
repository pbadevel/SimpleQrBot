from collections.abc import Sequence
from typing import Protocol, TypeVar

from sqlalchemy.orm import Mapped
from sqlalchemy.sql.base import ExecutableOption

from .protocol import RepositoryProtocol

ID_TYPE = TypeVar("ID_TYPE")


class ModelIDProtocol(Protocol[ID_TYPE]):
    id: Mapped[ID_TYPE]


Options = Sequence[ExecutableOption]


class RepositoryIDMixin[MODEL_ID: ModelIDProtocol, ID_TYPE]:
    async def get_by_id(
        self: RepositoryProtocol[MODEL_ID],
        id: ID_TYPE,
        *,
        options: Options = (),
    ) -> MODEL_ID | None:
        stmt = self.get_base_stmt().where(self.model.id == id).options(*options)

        return await self.get_one_or_none(stmt)

    async def get_one_by_id(
        self: RepositoryProtocol[MODEL_ID],
        id: ID_TYPE,
        *,
        options: Options = (),
    ) -> MODEL_ID:
        stmt = self.get_base_stmt().where(self.model.id == id).options(*options)

        return await self.get_one_or_raise(stmt)
