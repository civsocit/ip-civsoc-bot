"""A screen is a message with or without an inline keyboard."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Screen:
    """Base screen class with type hintings and universal method."""
    text: str = None
    reply_markup: InlineKeyboardMarkup = None

    def as_dict(self) -> dict:
        """
        Convert a screen to a dictionary for deployment when sending
        or editing a message.
        """
        return {'text': self.text,
                'reply_markup': self.reply_markup}


class Start(Screen):
    """Start menu."""
    def __init__(self, name: str):
        self.text = ('Привет, {}.\nЯ бот-помощник Фракции Защиты Интернета.\n'
                     'Чем могу быть полезен?').format(name)
        self._create_reply_markup()

    def _create_reply_markup(self):
        self.reply_markup = InlineKeyboardMarkup(2)

        self.reply_markup.row(
                InlineKeyboardButton('Вступить во фракцию',
                                     callback_data='unavailable'))
        self.reply_markup.add(
                InlineKeyboardButton('О фракции', callback_data='unavailable'),
                InlineKeyboardButton('О движении', callback_data='unavailable'),
                InlineKeyboardButton('Связаться с директоратом',
                                     callback_data='directors'),
                InlineKeyboardButton('Связаться с редакцией',
                                     callback_data='unavailable'))


class ContactSet(Screen):
    """
    The first message when trying to contact is with an explanation
    of what to do.
    """
    def __init__(self, recipient: str):
        self.text = 'Отправь сообщение и я перешлю его {}.'.format(recipient)
        self._create_reply_markup()

    def _create_reply_markup(self):
        self.reply_markup = InlineKeyboardMarkup()
        self.reply_markup.add(InlineKeyboardButton('<< Назад',
                                                   callback_data='start'))


class MessageForwarded(Screen):
    """
    A message that a message has been forwarded to a contact chat.
    """
    def __init__(self, recipient:str):
        self.text = 'Ваше сообщение отправлено {}.'.format(recipient)


class MessageFrom(Screen):
    """A message from a contact chat for a user."""
    def __init__(self, sender: str, text: str):
        self.text = ('#{}\n\n{}\n\n'
                '<i>Вы можете снова отправить сообщение, ответив на это.</i>')\
                .format(sender, text)
        self._create_reply_markup()
    
    def _create_reply_markup(self):
        self.reply_markup = InlineKeyboardMarkup()
        self.reply_markup.add(InlineKeyboardButton('<< В главное меню',
                                                   callback_data='start_new'))
