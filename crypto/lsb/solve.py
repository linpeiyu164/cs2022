from pwn import *
from Crypto.Util.number import long_to_bytes, getPrime
import math

r = remote('edu-ctf.zoolab.org', 10102)

n = int(r.recvline().decode().strip())
e = int(r.recvline().decode().strip())
c = int(r.recvline().decode().strip())

found_bits = []

count = int(math.log(n, 3))

for i in range(0, count):
    cipher = (c * pow(3, -e*i, n)) % n
    r.sendline(str(cipher).encode())
    lsb = int(r.recvline().decode().strip())
    subtract = 0
    for j in range(1, len(found_bits)+1):
        subtract += ((pow(3, -1*j, n) * found_bits[j-1]) % n)
    subtract %= n
    subtract %= 3
    lsb = (lsb - subtract) % 3
    found_bits = [lsb] + found_bits

found_bits.reverse()
m = 0
for i in range(len(found_bits)):
    m += pow(3, i) * found_bits[i]
    m %= n

flag = long_to_bytes(m)
print(flag)

#FLAG{lE4ST_519Nific4N7_Bu7_m0S7_1MporT4Nt}