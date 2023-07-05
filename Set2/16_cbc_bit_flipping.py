### Boilerplate
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from lib import *
###

global_key = generate_random_bytes(16)
global_iv = generate_random_bytes(16)
actual_prefix = "comment1=cooking%20MCs;userdata="
actual_suffix = ";comment2=%20like%20a%20pound%20of%20bacon"

def encryption_oracle(input):
    global global_key, global_iv
    input = input.replace(";", "%3B").replace("=", "%3D")
    prefix = "comment1=cooking%20MCs;userdata="
    suffix = ";comment2=%20like%20a%20pound%20of%20bacon"
    plaintext = bytes(prefix+input+suffix, "utf-8")
    padded_input = pad_PKCS7(plaintext, 16)
    ciphertext = encrypt_aes_128_cbc(padded_input, global_key, global_iv)
    return ciphertext

def is_admin_oracle(ciphertext):
    global global_key, global_iv
    plaintext = decrypt_aes_128_cbc(ciphertext, global_key, global_iv)
    unpadded = unpad_PKCS7(plaintext,16)
    print(unpadded)
    return unpadded.find(b";admin=true;") != -1


test = "0000000000000000"

actual_payload = actual_prefix + test + actual_suffix
split_text_into_blocks(actual_payload,16, True)

enc = encryption_oracle(test)

enc_blocks = split_text_into_blocks(enc, 16)
enc_blocks[1] = bytes_fixed_xor(bytes_fixed_xor(enc_blocks[1],b"0000000000000000"),b";admin=true;0000")

print(enc_blocks)
tampered_enc = join_blocks_into_text(enc_blocks)
print(is_admin_oracle(tampered_enc))