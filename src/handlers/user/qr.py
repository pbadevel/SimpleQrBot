from aiogram import Router, types, F

from src.database import SessionManager
from src.users.service import UserService
from src.middlewares import ChannelSubscriptionWare
from src.qr_code import qr_genetator
from src.logging import get_logger

from ..texts import (
    YOU_CANNOT_USE_QR,
    CAPTION_TO_THE_QR,
)

from ..types import UserCallbackActions
from ..utils import get_qr_payload_from_user



router = Router()
log = get_logger()


router.callback_query.outer_middleware(
    middleware=ChannelSubscriptionWare()
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