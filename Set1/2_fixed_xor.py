### Boilerplate
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from lib import *
###

def bytes_fixed_xor(a, b):
    return bytes([_a ^ _b for _a, _b in zip(a, b)])

# test1 = "1c0111001f010100061a024b53535009181c"
# test2 = "686974207468652062756c6c277320657965"
# print(bytestohex(bytes_fixed_xor(hextobytes(test1), hextobytes(test2))))