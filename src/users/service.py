from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.types import User as TGUser

from src.logging import get_logger
from src.models import User
from src.enums import UserRole
from src.config import settings

from .repository import UserRepository


log = get_logger()


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def resolve_from_tg_user(self, tg_user: TGUser) -> User:
        log.debug("Resolving user from telegram user", user_id=tg_user.id)

        if tg_user.is_bot:
            raise ValueError("Telegram user is bot.")

        repository = self.get_repository()
        user = await repository.get_by_id(id=tg_user.id)

        if user is None:
            log.info(
                "User not found in database, creating from telegram user",
                user_id=tg_user.id,
            )
            try:
                user = await repository.create(
                    User(
                        id=tg_user.id,
                        first_name=tg_user.first_name,
                        last_name=tg_user.last_name,
                        username=tg_user.username,
                        role=UserRole.USER if tg_user.id not \
                            in settings.bot.admin_ids else UserRole.ADMIN
                    )
                )
            except:
                user = await self.update_from_tg(tg_user)

        return user

    async def update_from_tg(
        self, tg_user: TGUser
    ) -> User:
        
        repository = self.get_repository()
        
        user = await repository.update(
            User,
            {
                "id":           tg_user.id,
                "first_name":   tg_user.first_name,
                "last_name":    tg_user.last_name,
                "username":     tg_user.username,
                "role":         UserRole.USER if tg_user.id not \
                                in settings.bot.admin_ids else UserRole.ADMIN
            },
        )

        return user
    
    async def update_qr_flag(
        self, user_id: int, flag: bool = True 
    ) -> User:
        repository = self.get_repository()
        
        user_instance = await repository.get_by_id(user_id) 
        
        if user_instance is None:
            raise ValueError(f"User with ID {user_id} not found")
        
        updated_user = await repository.update(
            user_instance, 
            {
                "qr_is_used": flag,
            },
        )
        return updated_user
    
    async def get_by_id(self, tg_id) -> User | None:
        repo = self.get_repository()
        
        user = await repo.get_by_id(tg_id)

        return user


    def get_repository(self) -> UserRepository:
        return UserRepository.from_session(self.session)
