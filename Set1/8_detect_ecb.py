### Boilerplate
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from lib import *
###

with open(f"C:\\Users\\Little Cat\\Desktop\\UniStud\\CryptoStuff\\CryptoPalsExcercises\\Set1\\8_data.txt", "r") as file:
    totalhex = "".join(file.readlines()).replace("\n", "")
    filebytes = hextobytes(totalhex)
    key = b"YELLOW SUBMARINE"
    # decrypted_bytes = decrypt_aes_128_ecb(filebytes, key)
    # blocks = [decrypted_bytes[i*16:(i+1)*16] for i in range(0, math.floor(len(decrypted_bytes)/16))]
    blocks = [filebytes[i*16:(i+1)*16] for i in range(0, math.floor(len(filebytes)/16))]
    count_dict = {}
    for block in blocks:
        if block in count_dict:
            count_dict[block] += 1
        else :
            count_dict[block] = 1
    
    print("Repeated hex ", sorted(count_dict.items(), key=lambda x:-x[1])[0][0].hex())

    