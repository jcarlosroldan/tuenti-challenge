enc = '3633363A33353B393038383C363236333635313A353336'
enc = [int(enc[i:i + 2], 16) for i in range(0, len(enc), 2)]

dec = '514;248;980;347;145;332'
dec = [ord(c) for c in dec]

key = [e ^ d for e, d in zip(enc, dec)]

enc2 = '3A3A333A333137393D39313C3C3634333431353A37363D'
enc2 = [int(enc2[i:i + 2], 16) for i in range(0, len(enc2), 2)]

dec = [e ^ k for e, k in zip(enc2, key)]

with open('key.txt', 'w') as fp:
	fp.write(bytes(dec).decode())