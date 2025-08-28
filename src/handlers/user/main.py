from aiogram import Router, types
from aiogram.filters.command import CommandStart, CommandObject

from src.database import SessionManager
from src.users.service import UserService
from src.logging import get_logger

from ..texts import (
    START_USER_MESSAGE,
    START_ADMIN_MESSAGE,
    CONFIRMATION_TEXT
)
from ..keyboard import show_qr, get_confirm_enterance_kb
from ..utils import decode_payload



router = Router()


log = get_logger()


@router.message(CommandStart())
async def start(message: types.Message, command: CommandObject):
    async with SessionManager.session() as session:
        service = UserService(session)
        user = await service.resolve_from_tg_user(message.from_user)

        if user:
            if user.is_admin:
                if command.args and user.is_admin:
                    payload = decode_payload(command.args)
                    log.info("Getted payload", payload=payload)
                    if payload.startswith('QR_'):
                        
                        user_from_payload_id = int(payload.split('_')[-1])
                        user_from_payload = await service.get_by_id(user_from_payload_id)

                        await message.answer(
                            text=CONFIRMATION_TEXT.format(
                                user_from_payload.link_to_user,
                                user_from_payload.fullname
                            ),
                            reply_markup = await get_confirm_enterance_kb(user_from_payload_id)
                        )
                        
                    return
                
                await message.answer(
                    text=START_ADMIN_MESSAGE.format(
                        user.name
                    )
                )

                return
                

            await message.answer(
                text=START_USER_MESSAGE.format(
                    user.name
                ),
                reply_markup=await show_qr()
            )
