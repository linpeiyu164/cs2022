# Match the function names with their hashed values
# Run: python3 find_function.py

def hash(name):
    tmp = 0
    for i in range(len(name)):
        tmp = 2 * ((ord(name[i]) | 0x60) + tmp)
    return tmp ^ 0xDEADBEEF

def to_upper_dll_name(name):
    upper = []
    nlen = len(name)
    for i in range(nlen):
        c = name[i]
        if( c >= 'a' and c <= 'z'):
            c = ord(c) - 32
            c = chr(c)
        upper.append(c)
    return upper

function_names = []

def check(name, value):
    if value == 0xDEABC9A9:
        print("func0: ", name)
    elif value == 0xDEAD6B8D:
        print("func1: ", name)
    elif value == 0xDEABC0F5:
        print("func2: ", name)
    elif value == 0xDE9AA037:
        print("func3: ", name)
    elif value == 0xDDEB1F21:
        print("func4: ", name)

f = open("kernel32.txt")
lines = f.readlines()

for line in lines:
    r = line.split(" ")[-1].strip()
    function_names.append(r)

for name in function_names:
    hashed = hash(name)
    check(name, hashed)