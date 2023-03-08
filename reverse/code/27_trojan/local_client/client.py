import socket
from Crypto.Util.number import bytes_to_long
from PIL import Image
import io

HOST = '127.0.0.1'
PORT = 19832

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
mystring = "cDqr0hUUz1".encode()
s.send(mystring)
dlen = bytes_to_long(s.recv(1024))

data = b''
while True:
    indata = s.recv(1024)
    if len(indata) == 0: # connection closed
        s.close()
        print('server closed connection.')
        break
    data += indata
data = bytearray(data)

key = "0vCh8RrvqkrbxN9Q7Ydx".encode()
key += b'\x00'
key = bytearray(key)


for i in range(len(data)):
    c = data[i]
    c = c ^ key[i % 21]
    data[i] = c

stream = io.BytesIO(data)
img = Image.open(stream)
img.save("test.png")
