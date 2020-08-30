"""User-side actions related to contact with directors."""
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message

from config import DIRECTORS_CHAT
from screens import ContactSet, MessageForwarded, Start
from states import Contact


async def set_directors_state(cq: CallbackQuery):
    """
    When user click on button 'Связаться с директоратом' in start
    menu.
    """
    await Contact.directors.set()
    await cq.message.edit_text(**ContactSet('директорам').as_dict())


async def directors_state(message: Message, state: FSMContext):
    """When user send message for directors."""
    await state.finish()
    await message.forward(DIRECTORS_CHAT)
    await message.answer(**MessageForwarded('директорату').as_dict())
    await message.answer(**Start(message.from_user.first_name).as_dict())
