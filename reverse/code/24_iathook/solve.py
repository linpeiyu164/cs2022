# Run: python3 solve.py

enc_flag = b'\x11\x3E\x2E\x29\x1C\x1E\x33\x3B\x31\x2F\x38\x3D\x04\x42\x2A\x32\x01\x1C\x0F\x00\x32\x30\x00\x16\x26\x2A'

def xor(name, xor_key):
    result = ""
    keylen = len(xor_key)
    for i in range(len(name)):
        c = name[i]
        k = xor_key[i % keylen]
        xor_result = chr(c ^ k)
        result += xor_result
    return result

wrong = bytes('Wrong', 'ascii')
wrong = bytearray(wrong)
result = xor(enc_flag, wrong)
print(result)