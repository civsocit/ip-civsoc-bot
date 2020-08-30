"""Временный стартовый модуль."""
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext

from config import TOKEN


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


logging.basicConfig(level=logging.DEBUG)


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Привет, {}.'.format(message.from_user.first_name))


if __name__ == '__main__':
    executor.start_polling(dp)
