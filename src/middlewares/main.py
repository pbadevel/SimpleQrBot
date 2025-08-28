from aiogram import BaseMiddleware, types
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from typing import (
    Any,  
    Callable, 
    Dict, 
    Awaitable,
)

from src.config import settings







class ChannelSubscriptionWare(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        try:
            if all([
                self.check_user_in_chat(
                    await self.get_user_status(event, chat_id)
                ) for chat_id in settings.bot.required_chats ]
                ):
                return await handler(event, data)
        
        except TelegramBadRequest:
            for admin_id in settings.bot.admin_ids:
                await event.bot.send_message(
                    chat_id=admin_id,
                    text = "Добавьте бота в канал с правами администратора!"
                )
            return
        except TelegramForbiddenError:
            for admin_id in settings.bot.admin_ids:
                await event.bot.send_message(
                    chat_id=admin_id,
                    text = "Уберите бота из черного списка в канале!"
                )
            return
        
        if isinstance(event, types.CallbackQuery):
            await event.message.answer(f'Вы не подписаны на <a href="{settings.bot.chat_link}"> КАНАЛ </a>\n\nПодпишитесь и попробуйте снова!')
        else:
            await event.answer(
                text=f'Вы не подписаны на <a href="{settings.bot.chat_link}"> КАНАЛ </a>\n\nПодпишитесь и попробуйте снова!'
            )

        
    async def get_user_status(self, event: types.TelegramObject, chat_id: int):
        return await event.bot.get_chat_member(
            chat_id=chat_id,
            user_id=event.from_user.id
        )
    

    def check_user_in_chat(self, u_status):
        if isinstance(u_status, types.ChatMemberMember) or isinstance(u_status, types.ChatMemberAdministrator) \
                or isinstance(u_status, types.ChatMemberOwner):
            return True
        return False