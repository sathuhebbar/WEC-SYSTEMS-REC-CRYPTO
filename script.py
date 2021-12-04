# We got the QR text from an online QR scanner.
# The image used is QR.jpg
# The QR text is in qrscan.txt.
with open('qrscan.txt', 'r') as f:
    p = f.read()

base64table = {}

# Generate table
for x in range(26):
    base64table[chr(0x41 + x)] = x
    base64table[chr(0x61 + x)] = x + 26

for x in range(10):
    base64table[str(x)] = 52 + x

# p is the line of text. It is Base64 code.
p = p[:-2]
u = ''

# Convert each character to the corresponding 6-bit binary
# integer and append to u.
for x in p:
    u += bin(base64table[x])[2:].rjust(6, '0')

# Extract 8 bit units from u and generate the next stage
p = ''
for j in range(0, len(u), 8):
    p += chr(int(u[j:j + 8], base=2))

with open('stage-1.txt', 'w') as f:
    f.write(p)

# Cipherous things start with the first 'P'
p = p[p.index('P'):]

# Caesar on p
with open('randomoutput', 'w') as f:
    for j in range(100):
        for x in p:
            # We're modding to get only lowercase letters
            f.write(chr(0x61 + (ord(x) + j) % 26))
        f.write('\n')

# Line 18 from the file looks useful
with open('randomoutput', 'r') as f:
    p = f.readlines()[17]

# Remove the newline
p = p[:-1]

# Write to file
with open('stage-2.txt', 'w') as f:
    f.write(p)

# There are too many 'x's. We will split by 'x'.
v = p.split('x')

# The cipher is the last piece
# Replace j with i
p = v[-1].replace('j', 'i')

# Letters without j
square = ["abcde", "fghik", "lmnop", "qrstu", "vwxyz"]

pos = {}
for i, s in enumerate(square):
    for j, x in enumerate(s):
        pos[x] = (i, j)

# get letter at required position
def getlet(x, y): return square[x][y]


# get position of required letter
def getpos(c):
    return pos[c]


u = ''
for j in range(0, len(p) - 1, 2):
    x1, y1 = getpos(p[j])
    x2, y2 = getpos(p[j + 1])
    if x1 == x2:
        u += getlet(x1, (y1 - 1) % 5)
        u += getlet(x1, (y2 - 1) % 5)
    elif y1 == y2:
        u += getlet((x1 - 1) % 5, y1)
        u += getlet((x2 - 1) % 5, y1)
    else:
        u += getlet(x1, y2) + getlet(x2, y1)

# Write to file
with open('stage-3.txt', 'w') as f:
    f.write(u)

# The message says RSA encrypt value 243 with N = 2419 and E = 11
# We need (243) ^ (11) % 2419
# 11 is small so no need for binexp
x = 1
for j in range(11):
    x = (x * 243) % 2419

# Write to file
with open('stage-4.txt', 'w') as f:
    f.write(str(x))

# PUT 1982 IN TO THE ZIP FILE!
# We have dontsee.txt now
with open('dontsee.txt', 'r') as f:
    p = f.read()

# Displacement check
with open('randomoutput1.txt', 'w') as f:
    for j in range(1, 10):
        for x in p:
            f.write(chr(ord(x) - j))
        f.write('\n')

# At line 5, that is, for j = 5, we have the message
with open('final.txt', 'w') as f:
    j = 5
    for x in p:
        f.write(chr(ord(x) - j))