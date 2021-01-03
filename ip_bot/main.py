import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from ip_bot.config import Config
from ip_bot.filters import register_filters
from ip_bot.handlers import register_handlers


config = Config.from_env()
logging.basicConfig(level=config.LOG_LEVEL)
bot = Bot(config.TOKEN, parse_mode='html')
bot.config = config
if config.REDIS_HOST and config.REDIS_PORT:
    storage = RedisStorage2(host=config.REDIS_HOST,
                            port=config.REDIS_PORT,
                            db=config.REDIS_INDEX,
                            password=config.REDIS_PASS)
else:
    storage = MemoryStorage()


dp = Dispatcher(bot, storage=storage)


async def on_startup(dp: Dispatcher):
    register_filters(dp)
    register_handlers(dp)
    await dp.bot.set_webhook(url=dp.bot.config.WEBHOOK_URL)


async def on_shutdown(dp: Dispatcher):
    if isinstance(dp.storage, RedisStorage2):
        await dp.storage.close()


def main():
    executor.start_webhook(dp, '/', on_startup=on_startup,
                           on_shutdown=on_shutdown)


if __name__ == '__main__':
    main()
