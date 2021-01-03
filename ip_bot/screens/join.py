from typing import Optional

from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           KeyboardButton,
                           ReplyKeyboardMarkup,
                           User)

from ip_bot.screens.base import BaseTextScreen


class Error(BaseTextScreen):
    def __init__(self):
        self.text = (
            'Я вас не понял. Попробуйте ещё раз.'
        )


class CharterDisagree(BaseTextScreen):
    def __init__(self):
        self.text = (
            'Вы не подтвердили согласие с уставом Фракции или Движения и не '
            'можете быть приняты.'
        )


class BaseStep(BaseTextScreen):
    def __init__(self, allow_skip: bool = False):
        self._create_reply_markup(allow_skip)

    def _create_reply_markup(self, allow_skip: bool = False):
        self.reply_markup = InlineKeyboardMarkup(1)
        if allow_skip:
            self.reply_markup.add(InlineKeyboardButton('Пропустить >',
                                                       callback_data='next'))
        self.reply_markup.add(
            InlineKeyboardButton('< Назад', callback_data='back'),
            InlineKeyboardButton('<< В главное меню', callback_data='start')
        )


class FullName(BaseTextScreen):
    def __init__(self):
        self.text = (
            'Нам нужны некоторая информация о вас.\n'
            'Не переживайте, мы гарантируем конфиденциальность ваших '
            'персональных данных.\n\n'
            'Для начала, пришлите <code>Фамилию Имя Отчество</code>.'
        )
        self._create_reply_markup()

    def _create_reply_markup(self):
        self.reply_markup = InlineKeyboardMarkup(1)
        self.reply_markup.add(
            InlineKeyboardButton(
                'Политика конфиденциальности',
                url='https://civsoc.net/politika-konfidencialnosti/'
            ),
            InlineKeyboardButton('<< Назад', callback_data='start')
        )


class Birthday(BaseStep):
    def __init__(self):
        self.text = (
            'А теперь дату вашего рождения в формате '
            '<code>ДД.ММ.ГГГГ</code>.'
        )
        super().__init__()


class Email(BaseStep):
    def __init__(self):
        self.text = (
            'Нам нужен ваш email в качестве альтернативного способа связи.'
        )
        super().__init__()


class CharterAgree(BaseTextScreen):
    def __init__(self, charter: str, charter_link: str):
        self.text = (
            'Согласны ли вы с уставом {}?'
        ).format(charter)
        self._create_reply_markup(charter_link)

    def _create_reply_markup(self, charter_link: str):
        self.reply_markup = InlineKeyboardMarkup(1)
        self.reply_markup.row(
            InlineKeyboardButton('Да', callback_data='yes'),
            InlineKeyboardButton('Нет', callback_data='no')
        )
        self.reply_markup.add(
            InlineKeyboardButton('Устав', url=charter_link),
            InlineKeyboardButton('< Назад', callback_data='back'),
            InlineKeyboardButton('<< В главное меню', callback_data='start')
        )


class About(BaseStep):
    def __init__(self):
        self.text = (
            'Напишите немного о себе. Чем вы могли бы помочь фракции? Не '
            'более 280 символов.'
        )
        super().__init__()


class IsCivsocMember(BaseTextScreen):
    def __init__(self):
        self.text = (
            'Являетесь ли вы членом движения "Гражданское Общество"?'
        )
        self._create_reply_markup()

    def _create_reply_markup(self):
        self.reply_markup = InlineKeyboardMarkup(1)
        self.reply_markup.row(
            InlineKeyboardButton('Да', callback_data='yes'),
            InlineKeyboardButton('Нет', callback_data='no')
        )
        self.reply_markup.add(
            InlineKeyboardButton('< Назад', callback_data='back'),
            InlineKeyboardButton('<< В главное меню', callback_data='start')
        )


class City(BaseStep):
    def __init__(self, allow_skip: bool):
        self.text = (
            'Федеральный совет хочет знать о вас чуть больше нас. Сообщите '
            'эти данные нам, а мы их передадим.\n'
            'В каком городе вы сейчас проживаете?'
        )
        super().__init__(allow_skip)


class PhoneNo(BaseTextScreen):
    def __init__(self, allow_skip: bool):
        self.text = (
            'Ещё им нужен номер телефона. Пожалуйста, отправьте его в '
            'международном формате.'
        )
        self._create_reply_markup(allow_skip)

    def _create_reply_markup(self, allow_skip: bool):
        self.reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
        self.reply_markup.add(KeyboardButton('Отправить контакт',
                                             request_contact=True))
        if allow_skip:
            self.reply_markup.add(KeyboardButton('Пропустить'))
        self.reply_markup.add(KeyboardButton('Назад'))
        self.reply_markup.add(KeyboardButton('/start'))


class Final(BaseTextScreen):
    def __init__(self):
        self.text = (
            'Спасибо, что доверили нам свои персональные данные. Ваша заявка '
            'на вступление принята к рассмотрению. Рекомендую удалить '
            'сообщения с личной информацией из чата и подписаться на наши '
            'соц.сети.'
        )
        self._create_reply_markup()

    def _create_reply_markup(self):
        self.reply_markup = InlineKeyboardMarkup(1)
        self.reply_markup.add(
            InlineKeyboardButton(
                'Telegram',
                url='https://t.me/civsoc_internet'
            ),
            InlineKeyboardButton(
                'Twitter',
                url='https://twitter.com/civsoc_internet'
            ),
            InlineKeyboardButton(
                'Instagram',
                url='https://www.instagram.com/civsoc_internet/'
            )
        )


class ToDirectors(BaseTextScreen):
    def __init__(self,
                 user: User,
                 full_name: str,
                 birthday: str,
                 email: str,
                 about: str,
                 is_civsoc_member: bool,
                 city: Optional[str] = None,
                 phone_no: Optional[str] = None,
                 **_):
        if user.username:
            name = '@' + user.username
        else:
            name = user.first_name

        if is_civsoc_member is True:
            is_civsoc_member = 'Да'
        if is_civsoc_member is False:
            is_civsoc_member = 'Нет'

        self.text = (
            f'Заявка от <a href="tg://user?id={user.id}">{name}</a>\n\n'
            f'<b>ФИО:</b> {full_name}\n'
            f'<b>Дата рождения:</b> {birthday}\n'
            f'<b>Email:</b> {email}\n'
            f'<b>Город:</b> {str(city)}\n'
            f'<b>Номер телефона:</b> {str(phone_no)}\n'
            f'<b>Член в ГрОба:</b> {is_civsoc_member}\n'
            f'<b>О себе:</b>\n{about}'
        )
