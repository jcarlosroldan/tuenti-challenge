# Tuenti Challenge Edition 6 Level 6
from PIL import Image
from numpy import array, zeros, average
from qrtools import QR

# clean QR code
img = Image.open("alice_shocked.png")
img = img.convert("L")
dirty = array(img)[:-1,:-1]
clean = zeros((29,29))

freqs = []
for y in range(29):
	for x in range(29):
		s = dirty[y*6:(y+1)*6, x*6:(x+1)*6]
		clean[y,x] = 255*(average(s)>128)

# read QR code
Image.fromarray(clean).convert("RGBA").save("clean.png")
qr = QR()
qr.decode("clean.png")
print(qr.data)

# interpreting the PIET program was done with npiet