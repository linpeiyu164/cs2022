from sage.all import *
from pwn import *
from Crypto.Util.number import long_to_bytes

r = remote('edu-ctf.zoolab.org', 10103)
p = 96456850819502697651206433361801612849694007439039534901275897822281008022426638029922804827957323939645650433553175342471778429701791876556731857837444487073451357781552072941643781181059225686915086570894391906713740074058071992761574468183289737131623956420664118596496095551605805183463515504965224966667
r.recvuntil('give me a prime')
r.sendline(str(p).encode())

F = GF(p, modulus='primitive')
b = F.gen()
r.recvuntil('give me a number')
r.sendline(str(b).encode())
r.recvuntil('The hint about my secret: ')
c = int(r.recvline().decode().strip())
x = discrete_log(c, b)
print(long_to_bytes(x))