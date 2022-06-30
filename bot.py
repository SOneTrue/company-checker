import asyncio
import warnings

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from loguru import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz_deprecation_shim import PytzUsageWarning

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.filters.logger import setup_logger
from tgbot.handlers.admin import register_admin
from tgbot.handlers.user import register_user
from tgbot.handlers.add_info import register_info
from tgbot.handlers.add_photo import register_photo
from tgbot.handlers.echo import register_echo
from tgbot.middlewares.db import DbMiddleware
from tgbot.misc.set_bot_commands import set_default_commands
from tgbot.services.writer_excel import write_info


def register_all_middlewares(dp):
    dp.setup_middleware(DbMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    register_info(dp)
    register_photo(dp)

    register_echo(dp)


def set_scheduled_jobs(scheduler, *args, **kwargs):
    scheduler.add_job(write_info, 'cron', day_of_week='mon-sun', hour=23, minute=00)


async def main():
    await setup_logger()

    config = load_config(".env")

    if config.tg_bot.use_redis:
        storage = RedisStorage2()
    else:
        storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    warnings.filterwarnings(action="ignore", category=PytzUsageWarning)
    scheduler = AsyncIOScheduler()

    bot['config'] = config

    register_all_middlewares(dp)
    register_all_filters(dp)
    await set_default_commands(dp)
    register_all_handlers(dp)

    set_scheduled_jobs(scheduler)
    # start
    try:
        scheduler.start()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
