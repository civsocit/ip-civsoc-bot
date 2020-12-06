"""User-side actions related to contact with redaction."""
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message

from ip_bot.screens import ContactSet, MessageForwarded, MessageFromUser, Start
from ip_bot.states import Contact


async def set_redaction_state(cq: CallbackQuery):
    """
    When user click on button 'Связаться с редакцией' in start menu.
    """
    await Contact.redaction.set()
    await cq.message.edit_text(**ContactSet('редакцией').as_dict())


async def redaction_state(message: Message, state: FSMContext):
    """When user send message for redaction."""
    await state.finish()
    await message.bot.send_message(
        chat_id=message.bot.config.REDACTION_CHAT,
        **MessageFromUser(message.from_user, message.text).as_dict()
    )
    await message.answer(**MessageForwarded('редакции').as_dict())
    await message.answer(**Start(message.from_user.first_name).as_dict())
