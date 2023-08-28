# -*- coding: utf-8 -*-
import logging
from aiogram import Dispatcher, executor, types
import os

import read_config
from bot import dp
from handlers import utils_handlers, bot_handlers

logging.basicConfig(level=logging.INFO)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    utils_handlers.register_utils_dp(dp)
    bot_handlers.register_bot_handlers(dp)

    executor.start_polling(dp, skip_updates=True)

