import base64

flag = "wcvGwPzT7+LY9PPo6eLY7vTY6ejz2OH15uDu6+LY5un+6uj14qmpqfo="
flag = base64.b64decode(flag)
flag_arr = bytearray(flag)
new_flag = ""
for b in flag:
    b ^= 135
    new_flag += chr(b)

print(new_flag)