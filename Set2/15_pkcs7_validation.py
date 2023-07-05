### Boilerplate
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from lib import *
###

def unpad_PKCS7(plaintext, blocksize):
    if len(plaintext)%blocksize != 0:
        raise Exception("invalid padding")
    for i in range(plaintext[-1]):
        if plaintext[-plaintext[-1]] != plaintext[-1]:
            raise Exception("invalid padding")
    return plaintext[:-plaintext[-1]]

# test = b"ICE ICE BABY ICE"
# padded = pad_PKCS7(test, 16)
# print(padded)
# unpadded = unpad_PKCS7(padded, 16)
# print(unpadded)

