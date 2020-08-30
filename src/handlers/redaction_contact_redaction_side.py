"""Redaction-side actions related to contact with redaction."""
from aiogram.types import Message

from screens import MessageFrom


async def redaction_reply(message: Message):
    """When redactor replied to message from user."""
    await message.bot.send_message(chat_id=message.reply_to_message.forward_from.id,
        **MessageFrom('Редакция', message.parse_entities()).as_dict())
