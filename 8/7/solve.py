from time import sleep
from base64 import b64decode
from PIL import Image

CHAR_SIZE = 24

im = Image.open('imgrip.png')
w, h = int(im.size[0] / 24), int(im.size[1] / CHAR_SIZE)

ocr = {}
text = ""
characters = list("cGlrYWNodSBwaXpIH2FjUgEgth1jk=")
for y in range(h):
	for x in range(w):
		char_img = im.crop((x * CHAR_SIZE, y * CHAR_SIZE, (x + 1) * CHAR_SIZE, (y + 1) * CHAR_SIZE))
		k = char_img.tobytes()
		if k not in ocr: ocr[k] = characters.pop(0)
		text += ocr[k]

text = b64decode(text).decode()
text = text.replace("pikachu", ".").replace("pikapi", ",").replace("pika", "[").replace("pipi", ">").replace("pichu", "<").replace("pi", "+").replace("ka", "-").replace("chu", "]")
with open("key.txt", "w") as fp:
	fp.write(text.replace(" ", "")[::-1])