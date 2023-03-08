from pwn import *

r = remote("edu-ctf.zoolab.org", 10006)
tcache_size = [0 for _ in range(7)]
tcache_bin = [[], [], []]
tcache_bin_count = [0, 0, 0]

# tcache chal

# malloc
for i in range(7):
    line = r.recvuntil(";").decode().strip()
    h = line.split('0x')[1][:-2]
    print("Size of ", chr(i+97), ": ", int(h, 16))
    tcache_size[i] = int(h, 16) - 0x8 + 0x10
    if tcache_size[i] % 0x10 != 0:
        tcache_size[i] = ((tcache_size[i] // 0x10) + 1) * 0x10

# free
for i in range(7):
    line = r.recvuntil(";").decode().strip()
    print(line)
    c = int(ord(line[5]) - ord('A'))
    if tcache_size[c] == 0x20:
        tcache_bin[0].append(c)
        tcache_bin_count[0] += 1
    elif tcache_size[c] == 0x30:
        tcache_bin[1].append(c)
        tcache_bin_count[1] += 1
    elif tcache_size[c] == 0x40:
        tcache_bin[2].append(c)
        tcache_bin_count[2] += 1

for idx in range(1, 3):
    ans = ""
    for i in range(len(tcache_bin[idx])):
        c = tcache_bin[idx][i] + ord('A')
    for i in range(len(tcache_bin[idx])-1, -1, -1):
        c = tcache_bin[idx][i] + ord('A')
        ans += chr(c)
        ans += " --> "
    ans += "NULL"
    print("Answer:", ans)
    r.sendlineafter("\n> ",ans.encode())

# address chal
r.recvuntil("\n----------- ** address chall ** -----------")
line = r.recvuntil(";").decode().strip()

cmp1 = ord(line.split("(")[1][1]) - ord('A')
addr = int(line.split("0x")[1][:12], 16)
print("Address: ", str(hex(addr)))
line = r.recvuntil("?").decode().strip()
cmp2 = ord(line[0]) - ord('A')

for i in range(cmp1, cmp2):
    addr += tcache_size[i]

ans = str(hex(addr))
r.sendlineafter("\n> ", ans.encode())

# index chal
xsize = int(r.recvuntil(";").decode().strip().split("0x")[1][0:2], 16)
ysize = int(r.recvuntil(";").decode().strip().split("0x")[1][0:2], 16)
idx = int(r.recvuntil(";").decode().strip()[2])
ans = xsize // 8 + idx + 2
r.sendlineafter("\n> ", str(ans).encode())

# tcache fd chal
r.recvuntil("assert")
addr = int(r.recvuntil(";").decode().strip().split("0x")[1][:12], 16)
addr = addr - xsize - 0x10
ans = str(hex(addr))
r.sendlineafter("\n> ", ans.encode())

# fastbin fd chall
r.recvuntil("assert")
addr = int(r.recvuntil(";").decode().strip().split("0x")[1][:12], 16)
addr = addr - xsize - 0x10 - 0x10
ans = str(hex(addr))
r.sendlineafter("\n> ", ans.encode())

r.interactive()
# FLAG{owo_212ad0bdc4777028af057616450f6654}
