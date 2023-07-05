### Boilerplate
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from lib import *
###
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
    return bytes_varlength_pad_xor(b, final_pad)
    
def check_bytes_eng_score(b):
    score = 0
    for i in range(len(b)-1):
        bigram = chr(b[i])+chr(b[i+1])
        bigram = bigram.lower()
        if bigram in bigram_freq:
            score += bigram_freq[bigram]
    return score

test = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
print(decrypt_onebytexor(hextobytes(test)))
