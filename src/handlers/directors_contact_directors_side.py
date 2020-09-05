"""Directors-side actions related to contact with directors."""
from aiogram.types import Message, MessageEntityType

from screens import MessageFromChat
from services import get_ids_from_text_mentions


async def directors_reply(message: Message):
    """When director replied to message from user."""
    ids = get_ids_from_text_mentions(message.reply_to_message)
    
    if len(ids) < 1:
        return

    await message.bot.send_message(chat_id=ids[0],
        **MessageFromChat('Директорат', message.parse_entities()).as_dict())
