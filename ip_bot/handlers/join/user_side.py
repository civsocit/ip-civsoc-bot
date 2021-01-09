import datetime
from typing import Union

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from ip_bot.screens import join as screens, RemoveReplyKeyboard, Start
from ip_bot.states import Join


async def full_name_question(cq: types.CallbackQuery):
    await Join.full_name.set()
    await screens.FullName.edit(cq.message)


async def get_full_name(message: types.Message, state: FSMContext):
    await state.update_data({'full_name': message.text})
    await Join.birthday.set()
    await screens.Birthday.send(message.bot, message.chat.id)


async def birthday_question(cq: types.CallbackQuery, state: FSMContext):
    await Join.birthday.set()
    await screens.Birthday.edit(cq.message)


async def get_birthday(message: types.Message, state: FSMContext):
    try:
        birthday = datetime.datetime.strptime(message.text, '%d.%m.%Y').date()
    except ValueError:
        await screens.Error.send(message.bot, message.chat.id)
        await screens.Birthday.send(message.bot, message.chat.id)
        return
    await state.update_data({'birthday': birthday})
    await Join.email.set()
    await screens.Email.send(message.bot, message.chat.id)


async def email_question(cq: types.CallbackQuery, state: FSMContext):
    await Join.email.set()
    await screens.Email.edit(cq.message)


async def get_email(message: types.Message, state: FSMContext):
    await state.update_data({'email': message.text})
    await Join.fraction_charter_agree.set()
    await screens.CharterAgree.send(
        message.bot, message.chat.id,
        charter='Фракции',
        charter_link=('https://civsoc.net/ustav-frakcii/'
                      'ustav-frakcii-zashchity-interneta/')
    )


async def fraction_charter_agree_question(cq: types.CallbackQuery,
                                          state: FSMContext):
    await Join.fraction_charter_agree.set()
    await screens.CharterAgree.edit(
        cq.message,
        charter='Фракции',
        charter_link=('https://civsoc.net/ustav-frakcii/'
                      'ustav-frakcii-zashchity-interneta/')
    )


async def get_fraction_charter_agree(cq: types.CallbackQuery,
                                     state: FSMContext):
    if cq.data == 'no':
        await state.finish()
        await screens.CharterDisagree.edit(cq.message)
        await Start.send(cq.bot, cq.message.chat.id,
                         name=cq.from_user.first_name)
        return
    await Join.about.set()
    await screens.About.edit(cq.message)


async def about_question(cq: types.CallbackQuery, state: FSMContext):
    await Join.about.set()
    await screens.About.edit(cq.message)


async def get_about(message: types.Message, state: FSMContext):
    if len(message.text) > 280:
        await screens.Error.send(message.bot, message.chat.id)
        await screens.About.send(message.bot, message.chat.id)
        return
    await state.update_data({'about': message.text})
    await Join.is_civsoc_member.set()
    await screens.IsCivsocMember.send(message.bot, message.chat.id)


async def is_civsoc_member_question(cq: types.CallbackQuery,
                                    state: FSMContext):
    await Join.is_civsoc_member.set()
    await screens.IsCivsocMember.edit(cq.message)


async def get_is_civsoc_member(cq: types.CallbackQuery, state: FSMContext):
    if cq.data == 'yes':
        allow_skip = True
        await state.update_data({'is_civsoc_member': True})
    if cq.data == 'no':
        allow_skip = False
        await state.update_data({'is_civsoc_member': False})
    await Join.city.set()
    await screens.City.edit(cq.message, allow_skip=allow_skip)


async def city_question(action: Union[types.CallbackQuery, types.Message],
                        state: FSMContext):
    data = await state.get_data()
    bot = action.bot
    if isinstance(action, types.CallbackQuery):
        message = action.message
    if isinstance(action, types.Message):
        message = action
    chat_id = message.chat.id
    await Join.city.set()
    await RemoveReplyKeyboard.send(bot, chat_id)
    allow_skip = data['is_civsoc_member']
    if isinstance(action, types.CallbackQuery):
        await screens.City.edit(message, allow_skip=allow_skip)
        return
    await screens.City.send(bot, chat_id)


async def get_city(message: types.Message, state: FSMContext):
    await state.update_data({'city': message.text})
    data = await state.get_data()
    await Join.phone_no.set()
    allow_skip = data['is_civsoc_member']
    await screens.PhoneNo.send(message.bot, message.chat.id,
                               allow_skip=allow_skip)


async def phone_no_question(cq: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await Join.phone_no.set()
    await cq.message.delete()
    allow_skip = data['is_civsoc_member']
    await screens.PhoneNo.send(cq.bot, cq.message.chat.id,
                               allow_skip=allow_skip)


async def get_phone_no(message: types.Message, state: FSMContext):
    phone_number = None
    bot = message.bot
    chat_id = message.chat.id
    data = await state.get_data()
    allow_skip = data['is_civsoc_member']
    await RemoveReplyKeyboard.send(message.bot, message.chat.id)

    if message.text:
        if message.text != 'Пропустить':
            phone_number = message.text
    if message.contact:
        phone_number = message.contact.phone_number

    if phone_number:
        await state.update_data({'phone_no': phone_number})

    if allow_skip:
        await state.finish()
        await screens.Final.send(bot, chat_id)
        await screens.ToDirectors.send(bot, bot.config.DIRECTORS_CHAT,
                                       user=message.from_user,
                                       phone_no=phone_number,
                                       **data)
        await Start.send(bot, chat_id, name=message.from_user.first_name)
        return

    await Join.civsoc_charter_agree.set()
    await screens.CharterAgree.send(
        message.bot, message.chat.id,
        charter='Движения',
        charter_link='https://civsoc.net/ustav-dvizheniya/'
    )


async def get_civsoc_charter_agree(cq: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    if cq.data == 'no':
        await screens.CharterAgree.edit(cq.message)
        await Start.send(cq.bot, cq.message.chat.id)
        return
    await screens.Final.edit(cq.message)
    await screens.ToDirectors.send(cq.bot, cq.bot.config.DIRECTORS_CHAT,
                                   **data)
    await Start.send(cq.bot, cq.message.chat.id, name=cq.from_user.first_name)


def register_cq(dp: Dispatcher):
    dp.register_callback_query_handler(full_name_question, text='join')


def register_cq_with_state(dp: Dispatcher):
    dp.register_callback_query_handler(full_name_question,
                                       state=Join.birthday, text='back')
    dp.register_callback_query_handler(birthday_question,
                                       state=Join.email, text='back')
    dp.register_callback_query_handler(email_question,
                                       state=Join.fraction_charter_agree,
                                       text='back')
    dp.register_callback_query_handler(fraction_charter_agree_question,
                                       state=Join.about, text='back')
    dp.register_callback_query_handler(get_fraction_charter_agree,
                                       state=Join.fraction_charter_agree)
    dp.register_callback_query_handler(about_question,
                                       state=Join.is_civsoc_member,
                                       text='back')
    dp.register_callback_query_handler(is_civsoc_member_question,
                                       state=Join.city,
                                       text='back')
    dp.register_callback_query_handler(get_is_civsoc_member,
                                       state=Join.is_civsoc_member)
    dp.register_callback_query_handler(city_question,
                                       state=Join.phone_no, text='back')
    dp.register_callback_query_handler(phone_no_question,
                                       state=Join.city, text='next')
    dp.register_callback_query_handler(phone_no_question,
                                       state=Join.civsoc_charter_agree,
                                       text='back')
    dp.register_callback_query_handler(get_civsoc_charter_agree,
                                       state=Join.civsoc_charter_agree)


def register_message_with_state(dp: Dispatcher):
    dp.register_message_handler(get_full_name, state=Join.full_name)
    dp.register_message_handler(get_birthday, state=Join.birthday)
    dp.register_message_handler(get_email, state=Join.email)
    dp.register_message_handler(get_about, state=Join.about)
    dp.register_message_handler(city_question,
                                state=Join.phone_no,
                                text='Назад')
    dp.register_message_handler(get_city, state=Join.city)
    dp.register_message_handler(
        get_phone_no,
        state=Join.phone_no,
        content_types=[ContentType.TEXT, ContentType.CONTACT]
    )
