"""Временный стартовый модуль."""
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import LOGGING_LEVEL, TOKEN
from filters import register_filters
from handlers import register_handlers


bot = Bot(TOKEN, parse_mode='html')
dp = Dispatcher(bot, storage=MemoryStorage())


logging.basicConfig(level=LOGGING_LEVEL.upper())


async def on_startup(dp: Dispatcher):
    register_filters(dp)
    register_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
