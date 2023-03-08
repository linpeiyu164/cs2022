# Find the correct module handle
# Run: python3 find_module_handle.py

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

dll_names = [
    "getprocaddress.exe",
    "vcruntime140d.dll",
    "ucrtbased.dll",
    "kernelbase.dll",
    "kernel32.dll",
    "ntdll.dll"
]

for dll_name in dll_names:
    upper_dll = to_upper_dll_name(dll_name)
    hashed_dll = hash(upper_dll)
    if hashed_dll == 0xdea0f067:
        print("Module handle: ", dll_name)
