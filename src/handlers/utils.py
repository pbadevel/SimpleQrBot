from src.models import User
from aiogram.utils.deep_linking import create_start_link, decode_payload
from src.kit.bot import get_bot




async def get_qr_payload_from_user(user: User):
    return await create_start_link(
        bot=get_bot(),
        payload="QR_" + str(user.id),
        encode=True
    )