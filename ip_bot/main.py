import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from ip_bot.config import Config
from ip_bot.filters import register_filters
from ip_bot.handlers import register_handlers


config = Config.from_env()
bot = Bot(config.TOKEN, parse_mode='html')
bot.config = config
dp = Dispatcher(bot, storage=MemoryStorage())


logging.basicConfig(level=config.LOG_LEVEL)


async def on_startup(dp: Dispatcher):
    register_filters(dp)
    register_handlers(dp)


def main():
    executor.start_polling(dp, on_startup=on_startup)


if __name__ == '__main__':
    main()
