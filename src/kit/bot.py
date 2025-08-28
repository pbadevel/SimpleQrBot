from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.config import settings


def get_bot() -> Bot:
    return Bot(
        token=settings.bot.token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
            link_preview_is_disabled=True    
        ),
    )
