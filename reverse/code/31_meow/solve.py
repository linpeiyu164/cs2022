# Run: python3 solve.py
enc_flag = b'\x24\x1D\x1B\x31\x21\x0B\x4F\x0F\xE8\x50\x37\x5B\x08\x40\x4A\x08\x1D\x11\x4A\xB8\x11\x67\x3F\x67\x38\x14\x3F\x19\x0B\x54\xB4\x09\x63\x12\x68\x2A\x45\x53\x0E'
enc_flag = bytearray(enc_flag)
key = b'\x62\x57\x56\x76\x64\x77\x3D\x3D\x87\x63\x00'
key = bytearray(key)

for i in range(len(enc_flag)):
    enc_flag[i] -= 2*(i % 3)
    enc_flag[i] ^= key[i % 11]
enc_flag = bytes(enc_flag)
print(enc_flag)