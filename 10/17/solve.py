from PIL import Image
from PIL.ImageChops import logical_and, logical_or, logical_xor, offset
from numpy.fft import fft, fftfreq
from matplotlib import pyplot as plt

# unscramble image
im = Image.open('zatoichi.png')
part_order = [3, 1, 0, 4, 5, 2]
pw = im.size[0] / 3
ph = im.size[1] / 2
parts = []
for col in range(3):
	for row in range(2):
		box = (pw * col, ph * row, pw * (col + 1), ph * (row + 1))
		parts.append(im.crop(box))
parts = [parts[p] for p in part_order]
for col in range(3):
	for row in range(2):
		box = (int(pw * col), int(ph * row))
		im.paste(parts[row * 3 + col], box)
im.save('zatoichi-unscrambled.png')

for bit in range(8):
	im2 = im.copy()
	for c in range(im.size[0]):
		for r in range(im.size[1]):
			im2.putpixel((c, r), tuple(255 * (channel & 2**bit) for channel in im.getpixel((c, r))))
	im2.save('bit_%d.png' % bit)
			

# save LSB data
data = []
for c in range(im.size[0]):
	for r in range(im.size[1]):
		data.extend(col % 2 for col in im.getpixel((c, r)))

# save LSB as binaries to visually inspect them
bts = [data[i:i + 8] for i in range(0, len(data), 8)]
little_endian_data = [sum(bit << b for b, bit in enumerate(byte)) for byte in bts]
with open('mistery_le', 'wb') as fp:
	fp.write(bytes(little_endian_data))
big_endian_data = [sum(bit << b for b, bit in enumerate(reversed(byte))) for byte in bts]
with open('mistery_be', 'wb') as fp:
	fp.write(bytes(big_endian_data))
'''
# create image of LSB channels
for n, col in enumerate(('r', 'g', 'b')):
	cols = data[n::3]
	im2 = im.copy()
	for r in range(im.size[1]):
		for c in range(im.size[0]):
			im2.putpixel((c, r), (255 * cols[r * im.size[0] + c],) * 3)
	im2.save('zatoichi-lsb_%s.png' % col)
'''
# hmmm... every LSB channel is a tiled 313x8px image
'''imgs = []
for n, (col, y_off) in enumerate((('r', 0), ('g', 5), ('b', 2))):
	cols = data[n::3]
	im2 = im.copy()
	for r in range(im.size[1]):
		for c in range(im.size[0]):
			im2.putpixel((c, r), (255 * cols[r * im.size[0] + c],) * 3)
	imgs.append(im2.crop((0, 0 + y_off, 313, 8 + y_off)).convert('1'))
imgs[0].save('braille/tile_r.png')
imgs[1].save('braille/tile_g.png')
imgs[2].save('braille/tile_b.png')

half = 313
for operation in (logical_and, logical_or, logical_xor):
	for g_shift_x in range(313):
		for g_shift_y in range(0, 8, 4):
			for b_shift_x in range(313):
				for b_shift_y in range(0, 8, 4):
					g = offset(imgs[1], g_shift_x, g_shift_y)
					b = offset(imgs[2], b_shift_x, b_shift_y)
					img = operation(operation(imgs[0], g), b)
					if all(img.getpixel((n, 0)) == img.getpixel((n, 4)) == 255 for n in range(313)) and sum(1 for n in range(313) for m in range(8) if img.getpixel((n, m)) == 0) > half or all(img.getpixel((n, 0)) == img.getpixel((n, 4)) == 0 for n in range(313)) and sum(1 for n in range(313) for m in range(8) if img.getpixel((n, m)) == 255) > half:
						img.save('braille/%s-g%dx-%dy-b%dx-%dy.png' % (operation.__name__, g_shift_x, g_shift_y, b_shift_x, b_shift_y))'''

#from numpy import correlate
#res = correlate(data, data)
'''print(len(data))

for n in range(3):
	subdata = data[n::3]
	print([n for n in range(len(subdata)) if subdata[:400] == subdata[n:n + 400]])'''

from collections import Counter
bts = [data[i:i + 8] for i in range(0, len(data), 8)]
little_endian_data = [sum(bit << b for b, bit in enumerate(byte)) for byte in bts]
print(Counter(little_endian_data).most_common(300))