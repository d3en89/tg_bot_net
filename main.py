# -*- coding: utf-8 -*-
import logging
from aiogram import Dispatcher, executor, types
import os

import read_config
from bot import dp
from handlers import utils_handlers, bot_handlers

logging.basicConfig(level=logging.INFO)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def access_enabled_id(func):
    """ Декоратор для проверки id который вызывает зендлер есть ли
        в списке разрешенных или нет """
    async def wrapper(message: types.Message):
        if read_config.watch_id(message.from_user.id):
            await func(message)
        else:
            await message.reply("Вашего ID нету в разрешенном списке")
    return wrapper


if __name__ == "__main__":
    utils_handlers.register_utils_dp(dp)
    bot_handlers.register_bot_handlers(dp)

    executor.start_polling(dp, skip_updates=True)

