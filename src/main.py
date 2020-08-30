"""Временный стартовый модуль."""
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext

from config import TOKEN
from filters import register_filters


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


logging.basicConfig(level=logging.DEBUG)


async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Привет, {}.'.format(message.from_user.first_name))


async def on_startup(dp: Dispatcher):
    register_filters(dp)
    dp.register_message_handler(start, chat_type='private', commands='start',
                                state='*')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
