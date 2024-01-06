from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

import read_config


bot_token = Bot(read_config.bot("token"))
if not bot_token:
    exit("Error: no token provided")


# Диспетчер для бота
storage_mem = MemoryStorage()
loops = asyncio.get_event_loop()
dp = Dispatcher(bot_token, storage=storage_mem, loop=loops)


def access_enabled_id(func):
    """ Декоратор для проверки id который вызывает зендлер есть ли
        ***функция устарела, теперь используется midleware
        в списке разрешенных или нет """
    async def wrapper(message: types.Message) -> str|bool:
        if read_config.watch_id(message.from_user.id):
            await func(message)
        else:
            await message.reply("Вашего ID нету в разрешенном списке")
    return wrapper
