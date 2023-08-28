from aiogram import Bot, Dispatcher, executor, types

import read_config


bot_token = Bot(read_config.bot("token"))
if not bot_token:
    exit("Error: no token provided")

# Диспетчер для бота
dp = Dispatcher(bot_token)
