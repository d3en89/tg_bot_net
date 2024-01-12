from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from db.my_redis_client import get_hash_command
from handlers.bot_handlers import cmd_start


def generate_value_keyboard(id_user, use_command: str):
    """ Генерируем кнопки из базы редис"""
    commands = get_hash_command(id_user, use_command.replace('/', ''))
    kb_client = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    if commands is not None:
        for i in range(len(commands)):
            buttons.append(commands[i])
    buttons.append('/cancel')
    kb_client.add(*buttons)
    return kb_client
