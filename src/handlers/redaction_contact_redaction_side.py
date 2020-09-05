"""Redaction-side actions related to contact with redaction."""
from aiogram.types import Message

from screens import MessageFromChat
from services import get_ids_from_text_mentions


async def redaction_reply(message: Message):
    """When redactor replied to message from user."""
    ids = get_ids_from_text_mentions(message.reply_to_message)

    if len(ids) < 1:
        return

    await message.bot.send_message(chat_id=ids[0],
        **MessageFromChat('Редакция', message.parse_entities()).as_dict())
