from aiogram import types

from ip_bot.screens import join
from ip_bot.screens.base import BaseTextScreen
from ip_bot.screens.remove_reply_keyboard import RemoveReplyKeyboard


__all__ = ['BaseTextScreen', 'RemoveReplyKeyboard', 'Start',
           'join', 'ContactSet',
           'MessageForwarded', 'MessageFromUser', 'MessageFromChat',
           'AboutCivsoc', 'AboutFraction']


class Start(BaseTextScreen):
    """Start menu."""
    def __init__(self, name: str):
        self.text = ('Привет, {}.\nЯ бот-помощник Фракции Защиты Интернета.\n'
                     'Чем могу быть полезен?').format(name)
        self._create_reply_markup()

    def _create_reply_markup(self):
        self.reply_markup = types.InlineKeyboardMarkup(2)

        self.reply_markup.row(
                types.InlineKeyboardButton('Вступить во фракцию',
                                           callback_data='join'))
        self.reply_markup.add(
            types.InlineKeyboardButton('О фракции',
                                       callback_data='about_fraction'),
            types.InlineKeyboardButton('О движении',
                                       callback_data='about_civsoc'),
            types.InlineKeyboardButton('Связаться с директоратом',
                                       callback_data='directors'),
            types.InlineKeyboardButton('Связаться с редакцией',
                                       callback_data='redaction')
        )


class ContactSet(BaseTextScreen):
    """
    The first message when trying to contact is with an explanation
    of what to do.
    """
    def __init__(self, recipient: str):
        self.text = 'Отправь сообщение и я перешлю его {}.'.format(recipient)
        self._create_reply_markup()

    def _create_reply_markup(self):
        self.reply_markup = types.InlineKeyboardMarkup()
        self.reply_markup.add(
            types.InlineKeyboardButton('<< Назад', callback_data='start')
        )


class MessageForwarded(BaseTextScreen):
    def __init__(self, recipient: str):
        self.text = 'Ваше сообщение отправлено {}.'.format(recipient)


class MessageFromUser(BaseTextScreen):
    """A message from a user for a contact chat."""
    def __init__(self, user: types.User, text: str):
        if user.username:
            name = '@' + user.username
        else:
            name = user.first_name
        self.text = 'От <a href="tg://user?id={}">{}</a>\n\n{}'.format(user.id,
                                                                       name,
                                                                       text)


class MessageFromChat(BaseTextScreen):
    def __init__(self, sender: str, text: str):
        self.text = (
            '#{}\n\n{}\n\n'
            '<i>Вы можете снова отправить сообщение, ответив на это.</i>')\
                .format(sender, text)
        self._create_reply_markup()

    def _create_reply_markup(self):
        self.reply_markup = types.InlineKeyboardMarkup()
        self.reply_markup.add(
            types.InlineKeyboardButton('<< В главное меню',
                                       callback_data='start_new')
        )


class AboutCivsoc(BaseTextScreen):
    """Section about civsoc."""
    def __init__(self):
        self.text = ('Мы — граждане Российской Федерации, с целью '
                     'восстановления народного суверенитета и предотвращения '
                     'узурпации власти, объявляем о формировании '
                     'всероссийского движения "Гражданское Общество".')
        self._create_reply_markup()

    def _create_reply_markup(self):
        self.reply_markup = types.InlineKeyboardMarkup()
        self.reply_markup.add(
            types.InlineKeyboardButton('Манифест',
                                       url='https://civsoc.net/our-manifest/'),
            types.InlineKeyboardButton(
                'Устав', url='https://civsoc.net/ustav-dvizheniya/'
            )
        )
        self.reply_markup.add(
            types.InlineKeyboardButton('<< Назад', callback_data='start')
        )


class AboutFraction(BaseTextScreen):
    """Section about fraction."""
    def __init__(self):
        self.text = ('Мы считаем свободу распространения и получения '
                     'информации главной ценностью сети Интернет.')
        self._create_reply_markup()

    def _create_reply_markup(self):
        self.reply_markup = types.InlineKeyboardMarkup()
        self.reply_markup.add(
            types.InlineKeyboardButton(
                'Манифест и устав',
                url=('https://civsoc.net/frakciya/'
                     'frakciya-zashchity-interneta/')
            )
        )
        self.reply_markup.row(
            types.InlineKeyboardButton('<< Назад', callback_data='start')
        )
