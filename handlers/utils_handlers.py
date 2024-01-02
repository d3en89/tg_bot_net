from aiogram import Dispatcher, types
import time
import subprocess
from bot import bot_token, access_enabled_id
from pythonping import ping
from typing import NoReturn
import read_config
from bot_utils import gen, get_speedtest, port_ping, my_nslook, zabbix_get


@access_enabled_id
async def check_ping(message: types.Message) -> NoReturn:
    get_message_bot: object = message.text.strip()
    mes = get_message_bot.split("/ping ")
    try:
        ip = mes[1]
        ping_ip = ping(ip, count=5)
    except IndexError:
        ping_ip = "Ошибка ввода адресса"
    except RuntimeError as e:
        e1 = e.args[0].split("\"")
        if e1[0] == "Cannot resolve address ":
             ping_ip = e1[0]
    await bot_token.send_message(message.chat.id, ping_ip, parse_mode="html")


@access_enabled_id
async def check_tracert(message: types.Message) -> NoReturn:
    get_message_bot: object = message.text.strip()
    mes = get_message_bot.split("/tracert ")
    ip = mes[1]
    start = subprocess.Popen(["traceroute", f"{ip}"], stdout=subprocess.PIPE)
    mas = []
    while start.poll() is None:
        output = start.stdout.readline()
        mas.append(output)
        if output == "b''":
            break
    ran = len(mas)
    for ind in range(ran - 1):
        str_ind = str(mas[ind]).replace("b'", "").replace("'", "")
        str_ind = str_ind.replace("\\n", "")
        await bot_token.send_message(message.chat.id, str_ind, parse_mode="html")
        time.sleep(1)


@access_enabled_id
async def check_speedtest(message: types.Message) -> NoReturn:
    await message.answer(f"Измирение скорости занимает от 1 до 3х минут ожидайте")
    speed = get_speedtest.check_speedtest()
    await bot_token.send_message(message.chat.id, speed , parse_mode="html")


@access_enabled_id
async def check_open_port(message: types.Message) -> NoReturn:
    get_message_bot: object = message.text.strip()
    mes = get_message_bot.split(" ")
    try:
        pping = port_ping.check_port(mes[1], int(mes[2]))
        await message.reply(pping)
    except IndexError:
        await message.reply("Введите корректные данные")


@access_enabled_id
async def check_dns_name(message: types.Message) -> NoReturn:
    get_message_bot: object = message.text.strip()
    mes = get_message_bot.split(" ")
    look = nslook.look_up(mes[1])
    if type(look) != list:
        await bot_token.send_message(message.chat.id, look, parse_mode="html")
    else:
        for i in look:
            await bot_token.send_message(message.chat.id, i, parse_mode="html")


@access_enabled_id
async def generate_pass(message: types.Message) -> NoReturn:
    get_message_bot: object = message.text.strip()
    mes = get_message_bot.split(" ")
    generate = gen.generator(mes[1:3])
    await bot_token.send_message(message.chat.id, generate)


@access_enabled_id
async def check_author_domain(message: types.Message) -> NoReturn:
    get_message_bot: object = message.text.strip()
    mes = get_message_bot.split(" ")
    try:
        if len(mes) > 3:
            raise IndexError("Вы ввели слишком много аргументов")
        if len(mes) < 2:
            raise IndexError("Вы ввели слишком мало аргументов")
        if len(mes) == 3:
            who = port_ping.whois_ianna(mes[1], mes[2])
        else:
            who = port_ping.whois_ianna(mes[1])
        if len(who) > 4096:
            for x in range(0, len(who), 4096):
                await bot_token.send_message(message.chat.id, who[x:x + 4096])
        else:
            await bot_token.send_message(message.chat.id, who, parse_mode="html")
    except IndexError as err:
        await bot_token.send_message(message.chat.id, "Не верно введены данные \n"
                                                      "введите /whois ip \n"
                                                      f"{err}", parse_mode="html")


@access_enabled_id
async def check_status_server(message: types.Message) -> NoReturn:
    get_message_bot: object = message.text.strip()
    mes = get_message_bot.split("/status ")
    if len(mes) == 1:
        search = "Не указан сервер после /status"
    else:
        search = zabbix_get(read_config.zabbix_data("server"),read_config.zabbix_data("user"),read_config.zabbix_data("password"),response=mes[1])
    await bot_token.send_message(message.chat.id, search, parse_mode="html")


def register_utils_dp(dp : Dispatcher) -> NoReturn:
    dp.register_message_handler(check_ping, commands=['ping'])
    dp.register_message_handler(check_speedtest, commands=['speedtest'])
    dp.register_message_handler(check_tracert, commands=['tracert'])
    dp.register_message_handler(check_open_port, commands=['pport'])
    dp.register_message_handler(check_dns_name, commands=['nslookup'])
    dp.register_message_handler(generate_pass, commands=['gen'])
    dp.register_message_handler(check_author_domain, commands=['whois'])
    dp.register_message_handler(check_status_server, commands=['status'])