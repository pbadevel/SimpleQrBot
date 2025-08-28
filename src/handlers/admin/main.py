from aiogram import Router, types, F

from src.database import SessionManager
from src.users.service import UserService
from src.middlewares import ChannelSubscriptionWare
from src.qr_code import qr_genetator

from ..texts import (
    USER_CANNOT_USE_QR,
    SMTH_WENT_WRONG,
    SUCCESS_UPDATED_USER_QR,
    SUCCESSED
)
from ..types import AdminCallbackActions



router = Router()



@router.callback_query(F.data.startswith('admin_'))
async def manage_user_callbacks(cb: types.CallbackQuery):
    action, user_id = cb.data.split('_')[-1].split(':')

    async with SessionManager.session() as session:
        service = UserService(session)
        await service.resolve_from_tg_user(cb.from_user)
        user = await service.get_by_id(int(user_id))


        if action == AdminCallbackActions.CONFIRM_ENTERANCE:

            if user.qr_is_used:
                await cb.answer(
                    text=USER_CANNOT_USE_QR,
                    show_alert=True
                )
                return
            
            user = await service.update_qr_flag(user_id=user.id, flag=True)
            
            await cb.answer()
            if user.qr_is_used:
                await cb.message.edit_text(
                    text = SUCCESS_UPDATED_USER_QR
                )
                return
            
            await cb.message.edit_text(
                text=SMTH_WENT_WRONG
            )

        elif action == AdminCallbackActions.REJECT_ENTERANCE:
            await cb.message.edit_text(
                text=SUCCESSED.format('отклонено')
            )
        else:
            await cb.message.edit_text(
                text=SUCCESSED.format('отменено')
            )