from typing import Any, Self, TypeVar

from sqlalchemy import Select, func, over, select
from sqlalchemy.ext.asyncio import AsyncSession

M = TypeVar("M")  # model


class BaseRepository[M]:
    model: type[M]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @classmethod
    def from_session(cls, session: AsyncSession) -> Self:
        return cls(session=session)

    async def get_one_or_none(self, stmt: Select[tuple[M]]) -> M | None:
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def get_one_or_raise(self, stmt: Select[tuple[M]]) -> M:
        result = await self.session.execute(stmt)
        return result.unique().scalar_one()

    async def get_all(self, stmt: Select[tuple[M]]) -> list[M]:
        result = await self.session.execute(stmt)
        return list(result.scalars().unique().all())

    async def paginate(
        self, stmt: Select[tuple[M]], limit: int, page: int
    ) -> tuple[list[M], int]:
        offset = (page - 1) * limit
        pagination_stmt: Select[tuple[M, int]] = (
            stmt.add_columns(over(func.count())).limit(limit).offset(offset)
        )
        results = await self.session.stream(pagination_stmt)

        items: list[M] = []
        count = 0

        async for result in results.unique():
            item, count = result._tuple()
            items.append(item)

        return items, count

    def get_base_stmt(self) -> Select[tuple[M]]:
        return select(self.model)

    async def create(
        self, obj: M, flush: bool = False, commit: bool = True, refresh: bool = False
    ) -> M:
        self.session.add(obj)
        await self.auto_save(flush=flush, commit=commit)

        if refresh:
            await self.session.refresh(obj)

        return obj

    async def update(
        self,
        obj: M,
        update_dict: dict[str, Any] | None = None,
        flush: bool = False,
        commit: bool = True,
        refresh: bool = False,
    ) -> M:
        if update_dict is not None:
            for attr, value in update_dict.items():
                setattr(obj, attr, value)

        self.session.add(obj)
        await self.auto_save(flush=flush, commit=commit)

        if refresh:
            await self.session.refresh(obj)

        return obj

    async def count(self, stmt: Select[tuple[M]]) -> int:
        count_stmt = stmt.with_only_columns(func.count())
        result = await self.session.execute(count_stmt)
        return result.scalar_one()

    async def delete(self, obj: M, flush: bool = False, commit: bool = True) -> None:
        await self.session.delete(obj)
        await self.auto_save(flush=flush, commit=commit)

    async def auto_save(self, flush: bool, commit: bool) -> None:
        if flush:
            await self.session.flush()
        if commit:
            await self.session.commit()
