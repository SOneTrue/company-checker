from aiogram import types
from loguru import logger


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("edit", "Поменять данные (вечер)"),
        ]
    )

    logger.info('Standard commands are successfully configured')
