### Boilerplate
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from lib import *
###

import random

def generate_random_bytes(count):
    return random.randbytes(count)

def aes_encryption_oracle(input_bytes):
    prefix = generate_random_bytes(random.randint(5,10))
    suffix = generate_random_bytes(random.randint(5,10))
    total_bytes = prefix+input_bytes+suffix
    padded_bytes = pad_PKCS7(total_bytes, 16)

    key = generate_random_bytes(16)
    iv = generate_random_bytes(16)
    mode = random.randint(1,2)

    if mode == 1: #ECB
        ciphertext = encrypt_aes_128_ecb(padded_bytes, key)
    elif mode == 2: #CBC
        ciphertext = encrypt_aes_128_cbc(padded_bytes, key, iv)

    return [ciphertext, mode]

def detect_mode_oracle(ciphertext):
    for offset in range(16):
        blocks = [ciphertext[i*16+offset:(i+1)*16+offset] for i in range(0, math.floor(len(ciphertext)/16))]
        appearance_list = []
        for block in blocks:
            if block in appearance_list:
                return "EBC"
            else:
                appearance_list.append(block)
        
    return "CBC" 

for i in range(10):
    encres = aes_encryption_oracle(b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    print(detect_mode_oracle(encres[0]), encres[1])
    