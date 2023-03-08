from sage.all import *
from pwn import *
from Crypto.Util.number import isPrime, getPrime

def find_weak_prime():
    p = 2
    while p.bit_length() < 1025:
        p *= getPrime(16)
        if p.bit_length() == 1024 and isPrime(p+1):
            return p + 1
    return -1

p = -1
while p == -1:
    p = find_weak_prime()
    if p != -1:
        print(p)
