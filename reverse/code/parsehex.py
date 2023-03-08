import sys

"""
Description:
    Parser tool to get hex data from IDA to a byte string for python
Usage:
    1. Undefine datatype in IDA
    2. Copy it to a input file
    3. Run parsehex
    4. Get the formatted byte string from output file
"""

if len(sys.argv) != 3:
    print("Usage: python3 parsehex.py <In File> <Out File>")

IN_FILE = sys.argv[1]
OUT_FILE = sys.argv[2]

infile = open(IN_FILE, 'r')
all_lines = infile.readlines()
outfile = open(OUT_FILE, 'w')
out = ""

for line in all_lines:
    if 'db' in line:
        line = line.split('db')[1]
        if 'h' in line:
            h = line.split('h')[0].strip()
            if len(h) == 3 and h[0] == '0':
                h = h[1:]
            out += ('\\x' + h)
        else:
            print(line)
            h = line.split(' ')[-1].strip()
            out += ('\\x0' + h)

outfile.write(out)