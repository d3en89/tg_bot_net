# -*- coding: utf-8 -*-
import logging
from pythonping import ping
from aiogram import Bot, Dispatcher, executor, types
import time
import subprocess
import read_config
import port_ping
import nslook
import gen
from get_zabbix import zabbix_get

# Объект бота
bot_token = Bot(read_config.bot("token"))
if not bot_token:
    exit("Error: no token provided")

# Диспетчер для бота
dp = Dispatcher(bot_token)

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Хэндлер на команду
@dp.message_handler(commands="help")
async def help_ans(message: types.Message):
    await message.reply(F' /ping  введите ip адрес(только ip адрес)\n' \
                        f'/id выдаст ваш id \n' \
                        f'/tracert  введите ip  адрес\n' \
                        f'/pport введите адрес хоста и номер порта, через пробел, который хотете проверить\n'\
	                f'/nslookup введите имя с указанием домена или IP-адрес\n'\
                        f'/gen введите кол-во сиволов в пароле и чере пробел введите y если нужно с символами \n'\
                        f'/status введите имя сервера для просмотра статуса \n' \
                        f'/start работа с кнопками \n' \
                        f'/stop удалить кнопки \n' \
                        )


### Получаем id пользователя
@dp.message_handler(commands=['id'])
async def alarm(message: types.Message):
    if read_config.watch_id(message.from_user.id) == True:
        await message.answer(f"Ваш ID: {message.from_user.id}\nВаш id добавлен в список разрешенных")
    else:
        await message.answer(f"Ваш ID: {message.from_user.id} Вам доступ запрещен")


@dp.message_handler(commands="ping")
async def mess(message):
    if read_config.watch_id(message.from_user.id) == True:
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
        await bot_token.send_message(message.chat.id, ping_ip, parse_mode='html')
    else:
        await message.answer(f"Ваш ID: {message.from_user.id} Вам доступ запрещен")


@dp.message_handler(commands="tracert")
async def mess(message):
    if read_config.watch_id(message.from_user.id) == True:
        get_message_bot: object = message.text.strip()
        mes = get_message_bot.split("/tracert ")
        ip = mes[1]
        start = subprocess.Popen(["traceroute", f'{ip}'], stdout=subprocess.PIPE)
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
            await bot_token.send_message(message.chat.id, str_ind, parse_mode='html')
            time.sleep(1)
    else:
        await message.answer(f"Ваш ID: {message.from_user.id} Вам доступ запрещен")


@dp.message_handler(commands='pport')
async def mess(message):
    if read_config.watch_id(message.from_user.id) == True:
        get_message_bot: object = message.text.strip()
        mes = get_message_bot.split(" ")
        try:
            pping = port_ping.check_port(mes[1], int(mes[2]))
            await message.reply(pping)
        except IndexError:
            await message.reply("Введите корректные данные")
    else:
        await message.answer(f"Ваш ID: {message.from_user.id} Вам доступ запрещен")


@dp.message_handler(commands="nslookup")
async def mess(message):
    if read_config.watch_id(message.from_user.id) == True:
        get_message_bot: object = message.text.strip()
        mes = get_message_bot.split(" ")
        print(mes)
        if not "." in mes[1]:
            mes[1] = f'{mes[1]}.local.domain'
        look = nslook.look_up(mes[1])
        await bot_token.send_message(message.chat.id, look, parse_mode='html')
    else:
        await message.answer(f"Ваш ID: {message.from_user.id} Вам доступ запрещен")


@dp.message_handler(commands="gen")
async def mess(message):
   if read_config.watch_id(message.from_user.id) == True:
       get_message_bot: object = message.text.strip()
       mes = get_message_bot.split(" ")
       generate = gen.generator(mes[1:3])
       await bot_token.send_message(message.chat.id, generate)
   else:
       await message.answer(f"Ваш ID: {message.from_user.id} Вам доступ запрещен")


@dp.message_handler(commands="status")
async def mess(message):
    if read_config.watch_id(message.from_user.id) == True:
        get_message_bot: object = message.text.strip()
        mes = get_message_bot.split("/status ")
        if len(mes) == 1:
            search = "Не указан сервер после /status"
        else:
            search = zabbix_get(read_config.zabbix_data("server"),read_config.zabbix_data("user"),read_config.zabbix_data("password"),response=mes[1])
        await bot_token.send_message(message.chat.id, search, parse_mode='html')
    else:
        await message.answer(f"Ваш ID: {message.from_user.id} Вам доступ запрещен")


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    if read_config.watch_id(message.from_user.id) == True:
        button1 = types.KeyboardButton("/help")
        kb_client = types.ReplyKeyboardMarkup()
        kb_client.add(button1)
        await message.answer("Выбирайте команду", reply_markup=kb_client)
    else:
        await message.answer(f"Ваш ID: {message.from_user.id} Вам доступ запрещен")


@dp.message_handler(commands="stop")
async def mess(message: types.Message):
    if read_config.watch_id(message.from_user.id) == True:
        return await message.answer(text="Кнопки удалены", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer(f"Ваш ID: {message.from_user.id} Вам доступ запрещен")


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

