### Boilerplate
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from lib import *
###

with open(f"C:\\Users\\Little Cat\\Desktop\\UniStud\\CryptoStuff\\CryptoPalsExcercises\\Set1\\4_data.txt", "r") as file:
    lines = file.readlines()
    decrypts = []
    i = 0
    for line in lines:
        decrypts.append([i,*decrypt_onebytexor(bytes.fromhex(line))])
        i+=1
    sorted = sorted(decrypts, key=lambda x: -x[1])[0:6]
    print(lines[sorted[0][0]])
    print(decrypts[sorted[0][0]])