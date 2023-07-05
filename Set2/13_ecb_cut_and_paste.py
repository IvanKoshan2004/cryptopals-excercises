### Boilerplate
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from lib import *
###

def parse_cookies(str):
    cookie_pairs = [cookie.split("=") for cookie in str.split("&")]
    result = {}
    for entry in cookie_pairs:
        if len(entry) == 2:
            result[entry[0]] = entry[1]
    return result

def profile_for(email):
    new_email = email.replace("&","").replace("=","").replace(" ","")
    string = "email="+new_email+"&uid=10&role=user"
    return string


key = generate_random_bytes(16)

def encrypt_profile_aes(email):
    plaintext = profile_for(email)
    padded = pad_PKCS7(bytes(plaintext, "utf-8"), 16)
    ciphertext = encrypt_aes_128_ecb(padded, key)
    return ciphertext

def decrypt_profile_aes(ciphertext):
    padded = decrypt_aes_128_ecb(ciphertext, key)
    return unpad_PKCS7(padded, 16)
def split_text_into_blocks(text, size, prints=False):

    blocks = [text[i*size:(i+1)*size] for i in range(math.ceil(len(text)/size))]
    if prints:
        for block in blocks:
            print(block)
    else:
        return blocks

# I don't really see how you can create a required block with current restrictions, so i will skip this one. Maybe will finish this later, though i got the idea
def get_tampered_ciphertext():
    req="ivan@gmail.com"
    treq1=b"ivan1234@gadmin\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b"
    ciph1 = encrypt_profile_aes(treq1)
    padded_profile = pad_PKCS7(bytes(profile_for(req), "utf-8"),16)
    split_text_into_blocks(padded_profile,16,True)

    p1 = "0123456789"

    print(profile_for(p1))


get_tampered_ciphertext()