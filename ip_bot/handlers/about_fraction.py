from aiogram.types import CallbackQuery

from screens import AboutFraction


async def about_fraction(cq: CallbackQuery):
    """When user click on button 'О фракции'."""
    await cq.message.edit_text(**AboutFraction().as_dict())
