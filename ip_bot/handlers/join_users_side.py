"""User-side actions related to join to fraction."""
from aiogram.types import CallbackQuery

from ip_bot.screens import Join
from ip_bot.states import Contact


async def set_join_state(cq: CallbackQuery):
    """
    When user click on button 'Вступить во фракцию' in start
    menu.
    """
    await Contact.directors.set()
    await cq.message.edit_text(**Join().as_dict())
