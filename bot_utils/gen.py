import random
from string import ascii_letters, digits, punctuation


def generator(arg: list) -> str:
    """ Псевддо генератор случайных паролей
    :param arg - принимает список по индексу arg[0] - количквство символов
                                             arg[1] - указатель "y" будут ли спец символы или нет
    """
    chars = [*ascii_letters, *digits]
    password = ''
    if len(arg) > 1 and arg[1] == "y":
        chars = [*chars, *punctuation]
    for i in range(int(arg[0])):
        password += random.choice(chars)

    return password
