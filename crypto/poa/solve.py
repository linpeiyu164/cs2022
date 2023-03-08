from re import L
from pwn import *

def print_str(flag):
    flg_str = ""
    for i in range(len(flag)):
        if 33 <= flag[i] < 128:
            flg_str += chr(flag[i])
    print(flg_str)

r = remote('edu-ctf.zoolab.org', 10101)
ct = r.recvline().decode().strip()
ct = bytes.fromhex(ct)
ct_orig_full = ct

full_flag = []
flag = []
BLOCK_LENGTH = 16
NUM_BLOCKS = int(len(ct) / BLOCK_LENGTH)

for blks in range(NUM_BLOCKS, 1, -1):
    ct_orig = ct_orig_full[:blks*BLOCK_LENGTH]
    # print(len(ct_orig))
    flag = []
    for x in range(17, 33):
        # x = 18
        ct = ct_orig
        for k in range(17, x):
            m = ct[-k]
            ct = ct[:-k] + xor(m, flag[-(k-16)], 0x00) + ct[-(k-1):]
        z = ct[-x]
        for c in range(129):
            ciphertxt = ct[:-x] + xor(z, c, 0x80) + ct[-(x-1):]
            r.sendline(ciphertxt.hex())
            res = r.recvline().decode().strip()
            if res == "Well received :)":
                print(c)
                flag = [c] + flag
                # print(len(flag))
                break
    full_flag = flag + full_flag
print_str(full_flag)
