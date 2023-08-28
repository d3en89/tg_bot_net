from aiogram import  Dispatcher, types

from read_config import watch_id
from bot import access_enabled_id


async def help_ans(message: types.Message):
    await message.reply(F"/ping  введите ip адрес(только ip адрес)\n" \
                        f"/id выдаст ваш id \n" \
                        f"/tracert  введите ip  адрес\n" \
                        f"/speedtest  вычислит скорость интернета\n" \
                        f"/pport введите адрес хоста и номер порта, через пробел, который хотете проверить\n"\
	                    f"/nslookup введите имя с указанием домена или IP-адрес\n"\
                        f"/gen введите кол-во сиволов в пароле и чере пробел введите y если нужно с символами \n"\
                        f"/whois введите ip  для получения информации по ip или домену,  если хотите получить \n"
                        f" расширенную информацию после ip или домена через пробел введите i \n"\
                        f"/status введите имя сервера для просмотра статуса \n" \
                        f"/start работа с кнопками \n" \
                        f"/stop удалить кнопки \n" \
                        )


async def get_id(message: types.Message):
    if watch_id(message.from_user.id):
        await message.answer(f"Ваш ID: {message.from_user.id}\nВаш id добавлен в список разрешенных")
    else:
        await message.answer(f"Ваш ID: {message.from_user.id}\nВам доступ запрещен")


@access_enabled_id
async def cmd_start(message: types.Message):
    button1 = types.KeyboardButton("/help")
    kb_client = types.ReplyKeyboardMarkup()
    kb_client.add(button1)
    await message.answer("Выбирайте команду", reply_markup=kb_client)


@access_enabled_id
async def cmd_stop(message: types.Message):
    return await message.answer(text="Кнопки удалены", reply_markup=types.ReplyKeyboardRemove())


def register_bot_handlers(dp : Dispatcher):
    dp.register_message_handler(help_ans, commands=["help"])
    dp.register_message_handler(get_id, commands=["id"])
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(cmd_stop, commands=["stop"])