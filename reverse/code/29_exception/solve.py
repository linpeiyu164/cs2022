# Run: python3 solve.py

enc_flag = b'\xE7\xE3\x72\x78\xAC\x90\x90\x7C\x90\xAC\xB1\xA6\xA4\x9E\xA7\xA2\xAC\x90\xB9\xB2\xBF\xBB\xBD\xB6\xAB\x90\xBA\xB4\x90\xBF\xC0\xC0\xC4\xCA\x95\xED\xC0\xB2'
enc_flag = bytearray(enc_flag)
b1 = 0xBE
b2 = 0xEF

for i in range(38):
    c = enc_flag[i]
    tmp = (b2 + i) & 0xFF
    c = (c - tmp) & 0xFF
    enc_flag[i] = c

for i in range(38):
    c = enc_flag[i]
    tmp = (b1 + i) & 0xFF
    c = (c ^ tmp) & 0xFF
    enc_flag[i] = c

print(bytes(enc_flag))