# Run: python3 solve.py

from scapy.all import *
from PIL import Image, ImageFile
import io
from Crypto.Util.number import bytes_to_long

key = '0vCh8RrvqkrbxN9Q7Ydx'.encode()
key += b'\x00'
key = bytearray(key)

f = rdpcap('log.pcapng')

data = b''
count = 0
for p in f:
    if p[TCP].payload:
        d = bytes(p[TCP].payload)
        if count >= 2:
            data += bytes(p[TCP].payload)
        else:
            count += 1

img_data = []
data = bytearray(data)

for i in range(len(data)):
    k = key[i % 21]
    c = data[i]
    c = k ^ c
    img_data.append(c)

img_data = bytes(img_data)
img_data = io.BytesIO(img_data)
ImageFile.LOAD_TRUNCATED_IMAGES = True
img = Image.open(img_data)
img.save("flag.png")