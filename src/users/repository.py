from sqlalchemy import func

from src.kit.repository import BaseRepository, RepositoryIDMixin
from src.models import User


class UserRepository(RepositoryIDMixin[User, int], BaseRepository[User]):
    model = User
    