from src.config import settings
from src.database import SessionManager
from src.logging import get_logger, configure
from src.handlers.admin import admin_router
from src.handlers.user import user_router, qr_router

configure(is_dev=True)

from src.kit.bot import get_bot
from aiogram import Dispatcher


log = get_logger()

import asyncio



async def main():
    log.info("Starting PBADEV SIMPLE QR Bot")
    log.info('Config loaded!', **settings.model_dump())

    session_manager = SessionManager.from_url(settings.database_url.get_secret_value())
    
    async with session_manager.connect() as conn:
        await session_manager.create_all(conn)

    log.info('Database is ready!')

    bot = get_bot()
    log.info('loaded bot', pm = bot.default)
    dispatcher = Dispatcher()

    dispatcher.include_routers(
        user_router,
        admin_router,
        qr_router
    )

    try:
        await dispatcher.start_polling(bot)
    except Exception as e:
        log.error("Error while pooling!", e=e)



    

if __name__ == "__main__":
    asyncio.run(main())
