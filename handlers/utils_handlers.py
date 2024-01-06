import asyncio

from aiogram import types,Dispatcher
from typing import NoReturn

from bot import bot_token, access_enabled_id, dp
import read_config
import bot_utils


async def check_speedtest(message: types.Message) -> NoReturn:
    await message.answer(f"Измирение скорости занимает от 1 до 3х минут ожидайте")
    a_speed = await dp.loop.create_task(bot_utils.get_speedtest())
    await bot_token.send_message(message.chat.id, f'Измерение скорости закончено:\n'
                                                  f'{a_speed}', parse_mode='html')


async def check_status_server(message: types.Message) -> NoReturn:
    get_message_bot = message.text.strip()
    mes = get_message_bot.split("/status ")
    if len(mes) == 1:
        search = "Не указан сервер после /status"
    else:
        search = bot_utils.zabbix_get(read_config.zabbix_data("server"),read_config.zabbix_data("user"),read_config.zabbix_data("password"),response=mes[1])
    await bot_token.send_message(message.chat.id, search, parse_mode='html')


def register_utils_handlers(dp: Dispatcher) -> NoReturn:
    dp.register_message_handler(check_speedtest, commands=['speedtest'])
    dp.register_message_handler(check_status_server, commands=['status'])

