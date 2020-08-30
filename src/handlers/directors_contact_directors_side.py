"""Directors-side actions related to contact with directors."""
from aiogram.types import Message

from screens import MessageFrom


async def directors_reply(message: Message):
    """When director replied to message from user."""
    await message.bot.send_message(chat_id=message.reply_to_message.forward_from.id,
        **MessageFrom('Директорат', message.parse_entities()).as_dict())
