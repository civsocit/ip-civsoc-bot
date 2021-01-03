from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message

from ip_bot.screens import RemoveReplyKeyboard, Start


async def start_cmd(message: Message, state: FSMContext):
    """Start screen handler by command."""
    await state.finish()
    await RemoveReplyKeyboard.send(message.bot, message.chat.id)
    screen = Start(message.from_user.first_name)
    await message.answer(**screen.as_dict())


async def start_cq(cq: CallbackQuery, state: FSMContext):
    """Start screen handler by callback query with edit message."""
    await state.finish()
    await RemoveReplyKeyboard.send(cq.bot, cq.message.chat.id)
    screen = Start(cq.from_user.first_name)
    await cq.message.edit_text(**screen.as_dict())


async def start_new_cq(cq: CallbackQuery, state=FSMContext):
    """Start screen handler by callback query with new message."""
    await state.finish()
    await cq.message.delete_reply_markup()
    await RemoveReplyKeyboard.send(cq.bot, cq.message.chat.id)
    screen = Start(cq.from_user.first_name)
    await cq.message.answer(**screen.as_dict())


def register_cq_with_state(dp: Dispatcher):
    dp.register_callback_query_handler(start_cq, state='*', text='start')
    dp.register_callback_query_handler(start_new_cq,
                                       state='*',
                                       text='start_new')


def register_cmd_with_state(dp: Dispatcher):
    dp.register_message_handler(start_cmd,
                                state='*',
                                commands='start',
                                chat_type='private')
