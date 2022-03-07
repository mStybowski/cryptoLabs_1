

f = open('sbox.SBX', 'rb') # opening a binary file
content = f.read() # reading all lines
mutable_bytes = bytearray(content)

functionsOutputs = [[],[],[],[],[],[],[],[]]
bytes = []
byteLength = 8



for x in mutable_bytes:
    byteString = bin(x)
    byteString = byteString[2:]
    byteString = byteString.zfill(byteLength)
    if byteString != '00000000':
        bytes.append(byteString)

print(len(bytes))

for bitIndex in range(0, 8):
    for x in bytes:
      functionsOutputs[bitIndex].append(x[bitIndex])

# print(functionsOutputs)
for func in functionsOutputs:
    print(func)
    print("===")