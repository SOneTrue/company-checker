from sqlite3 import IntegrityError

from aiogram import types
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.models.users import add_user


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    async def pre_process(self, obj, data, *args):
        telegram_user: types.User = obj.from_user
        user = await add_user(telegram_user.id,
                              username=telegram_user.username,
                              fname=telegram_user.first_name,
                              lname=telegram_user.last_name,
                              rname=None,
                              number_auto=None,
                              road_list=None,
                              odometer=None,
                              odometer_back=None,
                              litre_back=None,
                              )
        data['user'] = user
