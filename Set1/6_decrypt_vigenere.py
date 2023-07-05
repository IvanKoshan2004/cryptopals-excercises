### Boilerplate
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from lib import *
###

def hamming_distance(a, b):
    if len(a) != len(b):
        return "Error"
    xored = bytes_fixed_xor(a, b)
    bits = 0
    for byte in xored:
        bits += byte.bit_count()
    return bits

def decrypt_xor_with_varkeysize(b, low, high, probable_keysizes_length = 20, text_limit = 1000):
    probable_keysizes = []
    for keysize in range(low, high+1):
        distances = []
        for i in range(0, text_limit-2*keysize, keysize):
            first_chunk = b[i*keysize:(i+1)*keysize]
            second_chunk = b[(i+1)*keysize:(i+2)*keysize]
            if len(first_chunk) != len(second_chunk) or len(first_chunk) == 0:
                break
            distance = hamming_distance(first_chunk, second_chunk)
            distances.append(distance)
        if len(distances) == 0:
            continue
        distances_average = sum(distances) / len(distances)
        normalized_distance = distances_average / keysize
        probable_keysizes.append([keysize, normalized_distance])
    probable_keysizes = [x[0] for x in sorted(probable_keysizes, key=lambda x: x[1])][0:probable_keysizes_length]
    
    def recover_key_from_xor_with_keysize(b, keysize):
        ciphertext_blocks = []
        chop = True
        i = 0
        while chop:
            block = b[i*keysize:(i+1)*keysize]
            if len(block) == keysize:
                ciphertext_blocks.append(block)
                i+=1
            else:
                chop = False

        transposed_blocks = []
        for i in range(keysize):
            transposed_block = bytes([block[i] for block in ciphertext_blocks])
            transposed_blocks.append(transposed_block)
        decrypted_blocks = []
        for transposed_block in transposed_blocks:
            decrypted_blocks.append(decrypt_onebytexor(transposed_block))

        return bytes([x[1] for x in decrypted_blocks])
    
    keys = []
    for keysize in probable_keysizes: 
        key = recover_key_from_xor_with_keysize(b, keysize)
        keys.append(key)

    max_score = -10000
    actual_key = ""
    for key in keys:
        supply = b[0:text_limit]
        supplyDecrypted = bytes_varlength_pad_xor(supply, key)
        print(len(key))
        score = check_bytes_eng_score(supplyDecrypted)
        if max_score < score:
            max_score = score
            actual_key = key
    print("Chosen key size: ", len(actual_key))
    return bytes_varlength_pad_xor(b, actual_key)

with open(f"C:\\Users\\Little Cat\\Desktop\\UniStud\\CryptoStuff\\CryptoPalsExcercises\\Set1\\6_data.txt", "r") as file:
    totalbase64 = "".join(file.readlines()).replace("\n", "")
    filehex = base64tohex(totalbase64)
    filebytes = hextobytes(filehex)

    result = decrypt_xor_with_varkeysize(filebytes, 2,40)
    print(result)