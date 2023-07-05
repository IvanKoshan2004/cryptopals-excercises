import base64
import math
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

#all
def hextobase64b(hex):
    b = bytes.fromhex(hex)
    return base64.b64encode(b)

def base64tohex(text):
    b = base64.b64decode(text)
    return b.hex()

def hextobytes(hex):
    return bytes.fromhex(hex)

def bytestohex(b):
    return b.hex()

#chal 2
def bytes_fixed_xor(a, b):
    return bytes([_a ^ _b for _a, _b in zip(a, b)])

#chal 3
def bytes_varlength_pad_xor(b, pad):
    times_long = len(b) / len(pad)
    if times_long > 1:
        pad = pad * math.ceil(times_long)
    pad = pad[0:len(b)]
    return bytes_fixed_xor(b, pad)


def check_bytes_eng_score(b):
    bigram_freq = {
        "th": 3.882,
        "he": 3.681,
        "in": 2.283,
        "er": 2.178,
        "an": 2.140,
        "re": 1.749,
        "nd": 1.571,
        "on": 1.418,
        "en": 1.383,
        "at": 1.335,
        "ou": 1.285,
        "ed": 1.275,
        "ha": 1.274,
        "to": 1.169,
        "or": 1.151,
        "it": 1.134,
        "is": 1.109,
        "hi": 1.092,
        "es": 1.092,
        "ng": 1.053385,
        "oo": 1,
    }
    letterFrequency = {'E' : 12.0,
        'T' : 9.10,
        'A' : 8.12,
        'O' : 7.68,
        'I' : 7.31,
        'N' : 6.95,
        'S' : 6.28,
        'R' : 6.02,
        'H' : 5.92,
        'D' : 4.32,
        'L' : 3.98,
        'U' : 2.88,
        'C' : 2.71,
        'M' : 2.61,
        'F' : 2.30,
        'Y' : 2.11,
        'W' : 2.09,
        'G' : 2.03,
        'P' : 1.82,
        'B' : 1.49,
        'V' : 1.11,
        'K' : 0.69,
        'X' : 0.17,
        'Q' : 0.11,
        'J' : 0.10,
        'Z' : 0.07 
    }
    score = 0
    for i in range(len(b)-1):
        if not chr(b[i]).isprintable():
            score -= 0.01
            continue
        bigram = chr(b[i])+chr(b[i+1])
        bigram = bigram.lower()

        if bigram in bigram_freq:
            score += bigram_freq[bigram]
        if chr(b[i]).upper() in letterFrequency:
            score += letterFrequency[chr(b[i]).upper()]/10
    return score

def decrypt_onebytexor(b):
    entries = []
    for pad_val in range(0,256):
        pad = bytes([pad_val])
        xored = bytes_varlength_pad_xor(b, pad)
        score = check_bytes_eng_score(xored)
        entries.append([pad_val, score])

    max_score = 0
    max_pad_val = 0
    for entry in entries:
        if max_score < entry[1]:
            max_pad_val = entry[0]
            max_score = entry[1]
    final_pad = bytes([max_pad_val])
    return [max_score, max_pad_val, bytes_varlength_pad_xor(b, final_pad)]

#chal 7
def decrypt_aes_128_ecb(ciph, key):
    obj = Cipher(algorithm=algorithms.AES128(key),mode=modes.ECB())
    decryptor = obj.decryptor()
    decrypted = decryptor.update(ciph) + decryptor.finalize()
    return decrypted

#chal 9
def pad_PKCS7(bytes, block_size):
    padder = padding.PKCS7(block_size*8).padder()
    padded_data = padder.update(bytes) + padder.finalize()
    return padded_data

def unpad_PKCS7(padded_bytes, block_size):
    unpadder = padding.PKCS7(block_size*8).unpadder()
    bytes = unpadder.update(padded_bytes) + unpadder.finalize()
    return bytes

#chal 10

def cbc_encryption_generic(bytes, key, block_size, iv, encryption_function):
    if len(bytes)%block_size != 0:
        return "unpadded plaintext"
    ciphertext = b""
    last_block = iv
    for block_i in range(0, int(len(bytes)/block_size)):
        block = bytes[block_i*block_size : (block_i+1)*block_size]
        xored_block = bytes_fixed_xor(block, last_block)
        encrypted_block = encryption_function(xored_block, key)
        last_block = encrypted_block
        ciphertext += encrypted_block

    return ciphertext

def cbc_decryption_generic(bytes, key, block_size, iv, decryption_function):
    if len(bytes)%block_size != 0:
        return "invalid length ciphertext"
    plaintext = b""
    last_block = iv
    for block_i in range(0, int(len(bytes)/block_size)):
        block = bytes[block_i*block_size : (block_i+1)*block_size]
        decrypted_block = decryption_function(block, key)
        xored_block = bytes_fixed_xor(decrypted_block, last_block)
        last_block = block
        plaintext += xored_block

    return plaintext

def encrypt_aes_128_ecb(plain, key):
    obj = Cipher(algorithm=algorithms.AES128(key),mode=modes.ECB())
    encryptor = obj.encryptor()
    encrypted = encryptor.update(plain) + encryptor.finalize()
    return encrypted

def encrypt_aes_128_cbc(plain, key, iv):
    obj = Cipher(algorithm=algorithms.AES128(key),mode=modes.CBC(iv))
    encryptor = obj.encryptor()
    encrypted = encryptor.update(plain) + encryptor.finalize()
    return encrypted

def decrypt_aes_128_cbc(ciph, key,iv):
    obj = Cipher(algorithm=algorithms.AES128(key),mode=modes.CBC(iv))
    decryptor = obj.decryptor()
    decrypted = decryptor.update(ciph) + decryptor.finalize()
    return decrypted

#chal 11

def generate_random_bytes(count):
    return random.randbytes(count)

#chal 13

def split_text_into_blocks(text, size, prints=False):

    blocks = [text[i*size:(i+1)*size] for i in range(math.ceil(len(text)/size))]
    if prints:
        for block in blocks:
            print(block)
    else:
        return blocks
    
def join_blocks_into_text(blocks, prints=False):
    text = b"".join(blocks)
    if prints:
        print(text)
    else:
        return text
    
#chal 15

def unpad_PKCS7(padded_bytes, block_size):
    if len(padded_bytes)%block_size != 0:
        raise Exception("invalid padding")
    if padded_bytes[-1] > block_size:
        raise Exception("invalid padding")
    if padded_bytes[-padded_bytes[-1]] != padded_bytes[-1]:
        raise Exception("invalid padding")
    return padded_bytes[:-padded_bytes[-1]]
