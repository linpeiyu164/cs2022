# Run: python3 solve.py

from Crypto.Util.number import long_to_bytes
arr = [
    0x8D909984B8BEBAB3,
    0x8D9A929E98D18B92,
    0xD0888BD19290D29C,
    0x8C9DC08F978FBDD1,
    0xD9C7C7CCCDCB92C2,
    0xC8CFC7CEC2BE8D91,
    0xFFFFFFFFFFFFCF82
]

b = 0xFF
c = 0xFF00
d = ~0xFFFF

sum = 0
for i in range(len(arr)):
    last = arr[i] & b
    last_2 = arr[i] & c
    last = (last << 8)
    last_2 = (last_2 >> 8)
    arr[i] = arr[i] & d
    arr[i] += (last + last_2)
    arr[i] = -arr[i]
    arr[i] &= 0xFFFFFFFFFFFFFFFF
    sum += (arr[i] << ((i)*64))

flag = long_to_bytes(sum)
flag = flag[::-1]

print(flag)