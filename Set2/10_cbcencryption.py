### Boilerplate
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from lib import *
###

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


with open(f"C:\\Users\\Little Cat\\Desktop\\UniStud\\CryptoStuff\\CryptoPalsExcercises\\Set2\\10_data.txt", "r") as file:
    totalbase64 = "".join(file.readlines()).replace("\n", "")
    filehex = base64tohex(totalbase64)
    filebytes = hextobytes(filehex)
    key = b"YELLOW SUBMARINE"
    iv = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    plaintext = cbc_decryption_generic(filebytes, key, 16, iv, decrypt_aes_128_ecb)
    print(plaintext)