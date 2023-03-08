# Run: python3 solve.py

from Crypto.Util.number import long_to_bytes
enc_flag = 0xB5E58DBD5C46364E4E1E0E26A41E0E4E460616ACB43E4E16943E948C948C9C4EA48C2E468C6C

enc_flag = long_to_bytes(enc_flag)
enc_flag = bytearray(enc_flag)
for i in range(len(enc_flag)):
    enc_flag[i] ^= 0x87
    # rotate right by 3
    last_3 = enc_flag[i] & 0x7
    enc_flag[i] >>= 3
    last_3 <<= 5
    enc_flag[i] += last_3
print(bytes(enc_flag))