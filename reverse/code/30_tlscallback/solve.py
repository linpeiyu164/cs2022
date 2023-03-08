# Run: python3 solve.py

enc_flag = b'\x46\x99\xF7\x64\x1D\x79\x44\x22\xC1\xD3\x27\xCD\x31\xC1\xD9\x77\xEC\x7A\x75\x24\xBF\xDD\x24\xDD\x23\xB2\xCD\x7C\x02\x58\x46\x24\xAC\xD8\x21\xD1\x5D\xBC\xC5\x7C\x05\x6C\x48\x2B\xBB\xD5\x11\xCB\x35\xB6\xD9\x57\x0F\x60\x3F\x34\xFF\xEC'
key = b'\xDE\xAD\xBE\xBF'
enc_flag = bytearray(enc_flag)
key = bytearray(key)

for i in range(4):
  if i % 3 == 0:
    key[i] ^= 0xFF
  elif i % 3 == 1:
    key[i] ^= 0x63
  else:
    key[i] ^= 0x87

for i in range(58):
  j = i & 3
  enc_flag[i] = (enc_flag[i] - key[j]) & 0XFF
  if i % 3 == 0:
    enc_flag[i] ^= 0x63
  elif i % 3 == 1:
    enc_flag[i] ^= 0x87
  else:
    enc_flag[i] ^= 0xFF

print(bytes(enc_flag))