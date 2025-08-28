from typing import Protocol

from sqlalchemy import Select

from .base import M


class RepositoryProtocol(Protocol[M]):
    model: type[M]

    async def get_one_or_none(self, stmt: Select[tuple[M]]) -> M | None: ...

    async def get_one_or_raise(self, stmt: Select[tuple[M]]) -> M: ...

    async def get_all(self, stmt: Select[tuple[M]]) -> list[M]: ...

    async def paginate(
        self, stmt: Select[tuple[M]], *, limit: int, page: int
    ) -> tuple[list[M], int]: ...

    def get_base_stmt(self) -> Select[tuple[M]]: ...

    async def create(self, obj: M, *, flush: bool = False) -> M: ...
