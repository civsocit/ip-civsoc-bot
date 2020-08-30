"""User-side actions related to contact with redaction."""
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message

from config import REDACTION_CHAT
from screens import ContactSet, MessageForwarded, Start
from states import Contact


async def set_redaction_state(cq: CallbackQuery):
    """
    When user click on button 'Связаться с редакцией' in start menu.
    """
    await Contact.redaction.set()
    await cq.message.edit_text(**ContactSet('редакцией').as_dict())


async def redaction_state(message: Message, state: FSMContext):
    """When user send message for redaction."""
    await state.finish()
    await message.forward(REDACTION_CHAT)
    await message.answer(**MessageForwarded('редакции').as_dict())
    await message.answer(**Start(message.from_user.first_name).as_dict())
