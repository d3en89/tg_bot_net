import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import types
from typing import NoReturn
from bot import access_enabled_id, bot_token, dp
from bot_utils import (func_ping, func_check_port,
                       generator, get_whois_ianna,
                       look_up, check_tracert)


class CmdState(StatesGroup):
    enter_command = State()
    enter_ping = State()  #
    enter_pport = State()  #
    enter_nslookup = State() #
    enter_gen = State()  #
    enter_whois = State()  #
    enter_tracert = State() #


async def check_ping(message: types.Message) -> NoReturn:
    if len(message.text.split(" ")) == 1:
        await CmdState.enter_command.set()
        await message.reply(f'Введите имя сервера или ip')
    else:
        get_message_bot = message.text.strip()
        mes = get_message_bot.split("/ping ")
        ping_ip = func_ping(mes, fl="No state")
        await bot_token.send_message(message.chat.id, ping_ip, parse_mode='html')


async def cancel_message(message: types.Message, state: FSMContext) -> NoReturn:
    current_state = state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Отменено")


async def get_data(message: types.Message, state: FSMContext) -> NoReturn:
    ping_ip = func_ping(message.text, fl="State")
    await bot_token.send_message(message.chat.id, ping_ip, parse_mode='html')
    await state.finish()


# noinspection PyTypeChecker
async def check_open_port(message: types.Message, ) -> NoReturn:
    if len(message.text.split(" ")) == 1:
        await CmdState.enter_pport.set()
        await message.reply("Введите имя или ip сервера и порт")
    if len(message.text.split(" ")) > 1:
        get_message_bot = message.text.strip()
        mes = get_message_bot.split(" ")
        await message.reply(func_check_port(mes, fl="No state"))


async def get_pping_data(message: types.Message, state: FSMContext) -> NoReturn:
    if len(message.text.split(" ")) < 2:
        await message.reply('Введены не корректные данные')
        await CmdState.enter_pport.set()
        await message.reply("Введите имя или ip сервера и порт")
    else:
        pping = func_check_port(message.text.split(), fl="State")
        name_server = message.text.split(" ")
        await bot_token.send_message(message.chat.id, f'Server: {name_server[0]}\n'
                                                      f'Port: {name_server[1]}\n'
                                                      f'{pping}', parse_mode='html')
        await state.finish()


async def gen_pass(message: types.Message, ) -> NoReturn:
    if len(message.text.split(" ")) == 1:
        await CmdState.enter_gen.set()
        await message.reply("Введите кол-во символов\n"
                            "и через пробел y если нужны спецсимволы")
    if len(message.text.split(" ")) > 1:
        get_message_bot = message.text.strip()
        mes = get_message_bot.split(" ")
        generate = generator(mes[1:3])
        await message.reply(generate)


async def generate_pass(message: types.Message, state: FSMContext) -> NoReturn:
    get_message_bot = message.text.strip()
    mes = get_message_bot.split(" ")
    generate = generator(mes[0:2])
    await bot_token.send_message(message.chat.id, generate, parse_mode='html')
    await state.finish()


async def check_author_domain(message: types.Message) -> NoReturn:
    get_message_bot = message.text.strip()
    mes = get_message_bot.split(" ")
    if len(mes) > 1:
        try:
            if len(mes) > 3:
                raise IndexError('Вы ввели слишком много аргументов')
            if len(mes) < 2:
                raise IndexError('Вы ввели слишком мало аргументов')
            if len(mes) == 3:
                who = get_whois_ianna(mes[1], mes[2])
            else:
                who = get_whois_ianna(mes[1])
            if len(who) > 4096:
                for x in range(0, len(who), 4096):
                    await bot_token.send_message(message.chat.id, who[x:x + 4096])
            else:
                await bot_token.send_message(message.chat.id, who, parse_mode='html')
        except IndexError as err:
            await bot_token.send_message(message.chat.id, "Не верно введены данные \n"
                                                          "введите /whois ip \n"
                                                          f"{err}", parse_mode='html')

    if len(mes) == 1:
        await CmdState.enter_whois.set()
        await message.reply("Введите имя или ip сервера")


async def get_author(message: types.Message, state: FSMContext) -> NoReturn:
    mes = message.text.strip().split()
    try:
        if len(mes) == 2:
            who = get_whois_ianna(mes[0], mes[1])
        else:
            who = get_whois_ianna(mes[0])
        if len(who) > 4096:
            for x in range(0, len(who), 4096):
                await bot_token.send_message(message.chat.id, who[x:x + 4096])
        else:
            await bot_token.send_message(message.chat.id, who, parse_mode='html')
    except IndexError as err:
        await bot_token.send_message(message.chat.id, "Не верно введены данные \n"
                                                      "введите /whois ip \n"
                                                      f"{err}", parse_mode='html')
    await state.finish()


async def check_dns_name(message: types.Message) -> NoReturn:
    get_message_bot = message.text.strip()
    mes = get_message_bot.split(" ")
    if len(mes) > 1:
        look = look_up(mes[1])
        if type(look) == list:
            for i in look:
                if i != None:
                    await bot_token.send_message(message.chat.id, i, parse_mode='html')
        else:
            await bot_token.send_message(message.chat.id, str(look), parse_mode='html')

    if len(mes) == 1:
        await CmdState.enter_nslookup.set()
        await message.reply(f'Введите имя сервера или ip')


async def get_look_up(message: types.Message, state : FSMContext) -> NoReturn:
    get_message_bot = message.text.strip()
    mes = get_message_bot.split(" ")
    look = look_up(mes[0])
    if type(look) == list:
        for i in look:
            if i != None:
                await bot_token.send_message(message.chat.id, i, parse_mode='html')
    else:
        await bot_token.send_message(message.chat.id, str(look), parse_mode='html')

    await state.finish()


async def start_tracert(message: types.Message) -> NoReturn:
    get_message_bot = message.text.strip()
    mes = get_message_bot.split(" ")
    if len(mes) > 1:
        if len(mes) > 2:
            res: str = await dp.loop.create_task(check_tracert(mes[1], mes[2]))
        if len(mes) == 2:
            res: str = await dp.loop.create_task(check_tracert(mes[1]))
        await bot_token.send_message(message.chat.id, res, parse_mode='html')

    if len(mes) == 1:
        await CmdState.enter_tracert.set()
        await message.reply(f'Введите имя сервера или ip\n'
                            f'и если необходимо через пробел\n'
                            f'кол-во прыжков')


async def get_data_tracert(message: types.Message, state : FSMContext) -> NoReturn:
    get_message_bot = message.text.strip()
    mes = get_message_bot.split(" ")
    if len(mes) > 1:
        res: str = await check_tracert(mes[0], mes[1])
    else:
        res: str = await check_tracert(mes[0])

    await bot_token.send_message(message.chat.id, res, parse_mode='html')

    await state.finish()

def register_state_handlers(dp: Dispatcher) -> NoReturn:
    dp.register_message_handler(check_ping, commands=['ping'], state=None)
    dp.register_message_handler(cancel_message, state="*", commands='cancel')
    dp.register_message_handler(cancel_message, Text(equals="cancel", ignore_case=True), state="*")
    dp.register_message_handler(get_data, state=CmdState.enter_command)
    dp.register_message_handler(check_open_port, commands=['pport'], state=None)
    dp.register_message_handler(get_pping_data, state=CmdState.enter_pport)
    dp.register_message_handler(gen_pass, commands=['gen'])
    dp.register_message_handler(generate_pass, state=CmdState.enter_gen)
    dp.register_message_handler(check_author_domain, commands=['whois'])
    dp.register_message_handler(get_author, state=CmdState.enter_whois)
    dp.register_message_handler(check_dns_name, commands=['nslookup'])
    dp.register_message_handler(get_look_up, state=CmdState.enter_nslookup)
    dp.register_message_handler(start_tracert, commands=['tracert'])
    dp.register_message_handler(get_data_tracert, state=CmdState.enter_tracert)
