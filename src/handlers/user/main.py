from aiogram import Router, types, F
from aiogram.filters.command import CommandStart, CommandObject

from src.database import SessionManager
from src.users.service import UserService
from src.middlewares import ChannelSubscriptionWare
from src.qr_code import qr_genetator
from src.logging import get_logger

from ..texts import (
    START_USER_MESSAGE,
    YOU_CANNOT_USE_QR,
    CAPTION_TO_THE_QR,
    START_ADMIN_MESSAGE,
    CONFIRMATION_TEXT
)
from ..keyboard import show_qr, get_confirm_enterance_kb
from ..types import UserCallbackActions
from ..utils import get_qr_payload_from_user, decode_payload



router = Router()

router.callback_query.outer_middleware(
    middleware=ChannelSubscriptionWare()
)
router.message.outer_middleware(
    middleware=ChannelSubscriptionWare()
)

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


@router.callback_query(F.data.startswith('user_'))
async def manage_user_callbacks(cb: types.CallbackQuery):
    action = cb.data.split('_')[-1]

    async with SessionManager.session() as session:
        service = UserService(session)
        user = await service.resolve_from_tg_user(cb.from_user)

    if action == UserCallbackActions.SHOW_QR:
        log.info("Try to show qr", user = user)
        if user.qr_is_used:
            await cb.answer(
                text=YOU_CANNOT_USE_QR,
                show_alert=True
            )
            log.info('NOT Showed', user=user)
            return
        
        await cb.answer()
        await cb.message.answer_photo(
            photo = await qr_genetator.generate(
                payload=await get_qr_payload_from_user(user)
            ),
            caption=CAPTION_TO_THE_QR
        )
        log.info('Showed', user=user)