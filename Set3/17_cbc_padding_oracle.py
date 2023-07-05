### Boilerplate
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from lib import *
###

global_key = generate_random_bytes(16)

def encryption_oracle():
    global global_key
    string_choices = [
        "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
        "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
        "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
        "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
        "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
        "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
        "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
        "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
        "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
        "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"
    ]
    chosen_string = random.choice(string_choices)
    plaintext = hextobytes(base64tohex(chosen_string))
    padded = pad_PKCS7(plaintext, 16)
    iv = generate_random_bytes(16)
    ciphertext = encrypt_aes_128_cbc(padded, global_key, iv)
    return [ciphertext, iv]

def padding_oracle(ciphertext, iv):
    global global_key
    padded_plaintext = decrypt_aes_128_cbc(ciphertext, global_key, iv)
    try:
        unpad_PKCS7(padded_plaintext, 16)
    except Exception:
        return False
    return True


def modify_iv_bytes_for_next_padding(iv, index):
    for i in range(len(iv)-(index+1), len(iv)):
        iv[i] = iv[i]^(index+1)^(index+2)

def cbc_padding_oracle_decrypt(ciph, iv, block_size = 16):
    decrypted = b""
    ciphertext_blocks = split_text_into_blocks(ciph, block_size)
    decrypted_blocks = []
    for block in ciphertext_blocks:
        zeroing_iv = bytearray(block_size)
        for i in range(block_size):
            for byte in range(256):
                zeroing_iv[block_size-(i+1)] = byte
                is_valid_pad = padding_oracle(block, bytes(zeroing_iv))
                if is_valid_pad:
                    if i != block_size-1:
                        modify_iv_bytes_for_next_padding(zeroing_iv, i)
                    break

        actual_zeroing_iv = bytes_fixed_xor(zeroing_iv, b"\x10"*block_size)
        decrypted_block = bytes_fixed_xor(actual_zeroing_iv, iv)
        iv = block
        decrypted_blocks.append(decrypted_block)
            
    decrypted = join_blocks_into_text(decrypted_blocks)
    return decrypted

[ciph, iv] = encryption_oracle()
decryption = cbc_padding_oracle_decrypt(ciph, iv)
print(decryption)