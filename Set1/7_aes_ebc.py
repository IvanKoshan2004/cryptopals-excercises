### Boilerplate
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from lib import *
###
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def decrypt_aes_128_ecb(ciph, key):
    obj = Cipher(algorithm=algorithms.AES128(key),mode=modes.ECB())
    decryptor = obj.decryptor()
    decrypted = decryptor.update(ciph) + decryptor.finalize()
    return decrypted

with open(f"C:\\Users\\Little Cat\\Desktop\\UniStud\\CryptoStuff\\CryptoPalsExcercises\\Set1\\7_data.txt", "r") as file:
    totalbase64 = "".join(file.readlines()).replace("\n", "")
    filehex = base64tohex(totalbase64)
    filebytes = hextobytes(filehex)
    key = b"YELLOW SUBMARINE"
    print(decrypt_aes_128_ecb(filebytes, key))
