from aiogram.types import Message


async def get_chat_id_cmd(message: Message):
    """Get chat id by command."""
    await message.answer('ID: <code>{}</code>'.format(message.chat.id))
