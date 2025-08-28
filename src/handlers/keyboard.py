from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from .types import UserCallbackActions, AdminCallbackActions



async def show_qr():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Получить', callback_data=f'user_{UserCallbackActions.SHOW_QR}')]
        ]
    )


async def get_confirm_enterance_kb(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅', callback_data=f'admin_{AdminCallbackActions.CONFIRM_ENTERANCE}:{user_id}'),
                InlineKeyboardButton(text='❌', callback_data=f'admin_{AdminCallbackActions.REJECT_ENTERANCE}:{user_id}')
            ],
            [InlineKeyboardButton(text='Отмена', callback_data=f'admin_{AdminCallbackActions.CANCEL_ENTERANCE}:{user_id}')]
        ]
    )



async def get_reply_qr_show_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Мой QR-код')]
        ],
        resize_keyboard=True
    )