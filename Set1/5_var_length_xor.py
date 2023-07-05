### Boilerplate
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from lib import *
###

text = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
wanted = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
res = bytestohex(bytes_varlength_pad_xor(text, b"ICE"))
print(res==wanted)
for i in range(len(wanted)):
    if wanted[i] != res[i]:
        print(i, " ", wanted[i],res[i],"\n")