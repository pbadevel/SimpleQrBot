from datetime import UTC, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import User


def utc_now() -> datetime:
    return datetime.now(UTC)

