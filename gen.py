import random

def generator(arg: list):
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    symbols ='+-/*!&$#?=@<>'
    password = ''
    if len(arg) > 1 and arg[1] == "y":
        chars = chars + symbols
    for i in range(int(arg[0])):
        password += random.choice(chars)
    return password




    