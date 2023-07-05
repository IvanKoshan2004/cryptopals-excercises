### Boilerplate
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from lib import *
###

global_key = generate_random_bytes(16)
prefix = generate_random_bytes(random.randint(1,15))

def aes_ecb_encryption_oracle(input):
    global global_key, prefix
    secret = b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
    input += hextobytes(base64tohex(secret))
    padded_input = pad_PKCS7(prefix+input, 16)
    ciphertext = encrypt_aes_128_ecb(padded_input, global_key)
    return ciphertext

def decrypt_byte_by_byte_secret():

    #get prefix length
    first_prefix = b""
    ciph = aes_ecb_encryption_oracle(first_prefix)
    for i in range(16):
        first_prefix += b"a"
        new_ciph = aes_ecb_encryption_oracle(first_prefix)
        if new_ciph[0:16] == ciph[0:16]:
            first_prefix = first_prefix[1:]
            print("length ", len(first_prefix))
            break
        ciph = new_ciph

    #decrypt in the same fasion, but with prefiz
    no_prefix_ciphertext = aes_ecb_encryption_oracle(first_prefix+b"")
    print("no_prefix")
    no_prefix_ciphertext_blocks = [no_prefix_ciphertext[i*16:(i+1)*16] for i in range(0, math.floor(len(no_prefix_ciphertext)/16))][0:3]
    for block in no_prefix_ciphertext_blocks:
        print(block)
    tampered_bytes = bytearray(0)
    prefix_ciphertext = aes_ecb_encryption_oracle(first_prefix+bytes(16))
    print("prefix_ciphertext")
    blocks = [prefix_ciphertext[i*16:(i+1)*16] for i in range(0, math.floor(len(prefix_ciphertext)/16))][0:4]
    for block in blocks:
        print(block) 
    decrypted_bytes = b""
    decrypted_block = bytearray(0)
    
    for block_i in range(len(no_prefix_ciphertext_blocks)):
        decrypted_block = bytearray(0)
        for byte_i in range(16):
            tampered_bytes = bytearray(15-byte_i)
            expected_ciphertext = aes_ecb_encryption_oracle(first_prefix+bytes(tampered_bytes))
            expected_block = expected_ciphertext[16:32]
            tampered_bytes.extend(decrypted_block)
            tampered_bytes.append(0)
            for i in range(256):
                tampered_bytes[-1] = i
                tampered_ciphertext = aes_ecb_encryption_oracle(first_prefix+bytes(tampered_bytes))
                tampered_block = tampered_ciphertext[16:32]
                if tampered_block == expected_block:
                    print("Got byte ", byte_i)
                    decrypted_block.append(i)
                    break
        decrypted_bytes += decrypted_block
        break
    return decrypted_bytes

decrypted = decrypt_byte_by_byte_secret()
print(decrypted)