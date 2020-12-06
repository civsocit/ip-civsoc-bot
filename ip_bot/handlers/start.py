"""Start screen handlers."""
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message

from screens import Start


async def start_cmd(message: Message, state: FSMContext):
    """Start screen handler by command."""
    await state.finish()
    screen = Start(message.from_user.first_name)
    await message.answer(**screen.as_dict())


async def start_cq(cq: CallbackQuery, state: FSMContext):
    """Start screen handler by callback query with edit message."""
    await state.finish()
    screen = Start(cq.from_user.first_name)
    await cq.message.edit_text(**screen.as_dict())


async def start_new_cq(cq: CallbackQuery, state=FSMContext):
    """Start screen handler by callback query with new message."""
    await state.finish()
    screen = Start(cq.from_user.first_name)
    await cq.message.answer(**screen.as_dict())
