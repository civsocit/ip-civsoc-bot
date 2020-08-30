from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start():
    markup = InlineKeyboardMarkup(2)

    markup.row(InlineKeyboardButton('Вступить во фракцию',
                                    callback_data='unavailable'))
    markup.add(InlineKeyboardButton('О фракции', callback_data='unavailable'),
               InlineKeyboardButton('О движении', callback_data='unavailable'),
               InlineKeyboardButton('Связаться с директоратом',
                                    callback_data='unavailable'),
               InlineKeyboardButton('Связаться с редакцией',
                                    callback_data='unavailable'))

    return markup
