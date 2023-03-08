from sage.all import *

output = [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0]
MASK = 0x1da785fc480000001
state = 0
print("output: ", output[-70:])

def create_relation_matrix(R, number):
    global MASK
    mask = MASK
    rows = []
    for i in range(64):
        v = [0 for i in range(64)]
        v[63] = mask & 1
        mask >>= 1
        if i != 0:
            v[i-1] = 1
        rows.append(v)
    A = matrix(R, rows)
    I = matrix.identity(R, 64)
    for _ in range(number):
        I *= A
    return I

def get_last_row(M):
    return M[63]

def getbit():
    global state
    state <<= 1
    if state & (1 << 64):
        state ^= MASK
        return 1
    return 0

R = IntegerModRing(2)
M = matrix.identity(R, 64)

k = 0
rows = []
A = create_relation_matrix(R, 36)
M = A * M
v = get_last_row(M)
rows.append(v)
k += 1

A = create_relation_matrix(R, 37)
while k < len(output):
    M = A * M
    v = get_last_row(M)
    rows.append(v)
    k += 1

b = vector(R, output[-70:])
M = Matrix(R, rows[-70:])
seed = M.solve_right(b)

seed = list(seed)
for i in range(len(seed)):
    state += (int(seed[i]) << i)

out = []
for i in range(len(output)):
    for __ in range(36):
        getbit()
    a = getbit()
    out.append(a)
    output[i] ^= a

count = 0
flag_str = ""
for i in range(len(output)-70):
    val = output[i] << (7 - (i % 8))
    count += val
    if i % 8 == 7:
        flag_str += chr(count)
        count = 0

print("output: ", out[-70:])
print(flag_str)
