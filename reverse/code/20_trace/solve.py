# Run: python3 solve.py

from Crypto.Util.number import long_to_bytes
enc_flag = 0x0C3F30122E242E37402E423C2E42123003250A36303D37
enc_flag = long_to_bytes(enc_flag)
enc_flag = bytearray(enc_flag)

for i in range(len(enc_flag)):
    enc_flag[i] ^= 0x71
flag = bytes(enc_flag[::-1])
print(flag)