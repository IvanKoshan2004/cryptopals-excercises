import base64

def hextobase64b(hex):
    b = bytes.fromhex(hex)
    return base64.b64encode(b)

def base64btohex(enc):
    b = base64.b64decode(enc)
    return b
# test = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
# print(hextobase64b(test))