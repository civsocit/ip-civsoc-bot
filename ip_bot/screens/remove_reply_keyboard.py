from aiogram.types import ReplyKeyboardRemove

from ip_bot.screens.base import BaseTextScreen


class RemoveReplyKeyboard(BaseTextScreen):
    @classmethod
    async def send(cls, *args, **kwargs):
        message = await super(RemoveReplyKeyboard, cls).send(*args, **kwargs)
        await message.delete()

    def __init__(self):
        self.text = '<i>Удаление клавиатуры...</i>'
        self.reply_markup = ReplyKeyboardRemove()
