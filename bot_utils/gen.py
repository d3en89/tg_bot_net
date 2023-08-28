import random
from string import ascii_letters, digits, punctuation

def generator(arg: list):
    chars = [*ascii_letters, *digits]
    password = ''
    if len(arg) > 1 and arg[1] == "y":
        chars = [*chars, *punctuation]
    for i in range(int(arg[0])):
        password += random.choice(chars)
    return password
