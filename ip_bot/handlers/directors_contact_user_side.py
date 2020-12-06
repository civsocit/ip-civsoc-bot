"""User-side actions related to contact with directors."""
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message

from screens import ContactSet, MessageForwarded, MessageFromUser, Start
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
    await message.bot.send_message(chat_id=message.bot.config.DIRECTORS_CHAT,
            **MessageFromUser(message.from_user, message.text).as_dict())
    await message.answer(**MessageForwarded('директорату').as_dict())
    await message.answer(**Start(message.from_user.first_name).as_dict())
