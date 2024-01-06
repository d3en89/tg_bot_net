# -*- coding: utf-8 -*-
import logging
from handlers import bot_handlers, utils_handlers, utils_with_state, my_errors_handlers

from bot import dp


# noinspection PyUnreachableCode
def register_handlers():
    ## Регестрируем наши хендлеры
    bot_handlers.register_bot_handlers(dp)
    my_errors_handlers.register_error_handler(dp)
    utils_handlers.register_utils_handlers(dp)
    utils_with_state.register_state_handlers(dp)


# # Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    import os
    from aiogram import executor

    os.chdir(os.getcwd())
    register_handlers()
    # Запуск бота
    executor.start_polling(dp, skip_updates=False)

