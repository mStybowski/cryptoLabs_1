# Python. Work with binary files

# Open binary file for reading
f = open('sbox.SBX', 'rb')

# Get a string from binary file
d = f.read()

# Display this string.
# The output will be as a string of characters
print("d = ", d) # d = b'\x80\x03]q\x00(K\x01\x88G@\x07\n=p\xa3\xd7\ne.'

# If print as a separate character,
# then the character code will be displayed - as an integer
print("d[5] = ", d[5]) # d[5] = 40
print("d[0] = ", d[0]) # d[0] = 128

# Use bin function for single character
print(bin(d[2])) # 0b1011101
f.close()