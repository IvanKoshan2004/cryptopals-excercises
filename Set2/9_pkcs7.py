### Boilerplate
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from lib import *
###

from cryptography.hazmat.primitives import padding

def pad_PKCS7(bytes, block_size):
    padder = padding.PKCS7(block_size*8).padder()
    padded_data = padder.update(bytes) + padder.finalize()
    return padded_data

def unpad_PKCS7(padded_bytes, block_size):
    unpadder = padding.PKCS7(block_size*8).unpadder()
    bytes = unpadder.update(padded_bytes) + unpadder.finalize()
    return bytes

test = b"YELLOW SUBMARINE"

print(pad_PKCS7(test, 16))