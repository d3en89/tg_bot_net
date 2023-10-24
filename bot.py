from aiogram import Bot, Dispatcher, executor, types

import read_config


bot_token = Bot(read_config.bot("token"))
if not bot_token:
    exit("Error: no token provided")

# Диспетчер для бота
dp = Dispatcher(bot_token)

def access_enabled_id(func):
    """ Декоратор для проверки id который вызывает зендлер есть ли
        в списке разрешенных или нет """
    async def wrapper(message: types.Message) -> str|bool:
        if read_config.watch_id(message.from_user.id):
            await func(message)
        else:
            await message.reply("Вашего ID нету в разрешенном списке")
    return wrapper
