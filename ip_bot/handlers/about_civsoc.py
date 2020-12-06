from aiogram.types import CallbackQuery

from ip_bot.screens import AboutCivsoc


async def about_civsoc(cq: CallbackQuery):
    """When user click on button 'О движении'."""
    await cq.message.edit_text(**AboutCivsoc().as_dict())
