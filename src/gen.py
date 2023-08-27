import random
import random
from string import ascii_lowercase, ascii_uppercase, digits, punctuation


def generator(arg: list):
    # chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    # symbols ='+-/*!&$#?=@<>'
    chars = ascii_lowercase+ascii_uppercase+digits+'0'
    symbols = punctuation
    password = ''
    if len(arg) > 1 and arg[1] == "y":
        chars = chars + symbols
    for i in range(int(arg[0])):
        password += random.choice(chars)
    return password
