from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ip_bot.screens.base import BaseTextScreen


class Start(BaseTextScreen):
    """Start menu."""
    def __init__(self, name: str):
        self.text = (
            f'Привет, {name}.\n'
            f'Я бот-помощник Фракции Защиты Интернета.\n'
            f'Чем могу быть полезен?'
        )
        self._create_reply_markup()

    def _create_reply_markup(self):
        self.reply_markup = InlineKeyboardMarkup(2)

        self.reply_markup.row(
            InlineKeyboardButton('Вступить во фракцию', callback_data='join')
        )
        self.reply_markup.add(
            InlineKeyboardButton('О фракции', callback_data='about_fraction'),
            InlineKeyboardButton('О движении', callback_data='about_civsoc'),
            InlineKeyboardButton('Связаться с директоратом',
                                 callback_data='directors'),
            InlineKeyboardButton('Связаться с редакцией',
                                 callback_data='redaction')
        )
