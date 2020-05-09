from math import sqrt
from random import choice
from re import escape
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep
import cv2 as cv
import numpy as np

# ------------------------------- CONSTANTS -----------------------------------

IP = "52.49.91.111"
PORT = 3456
BUFFER_SIZE = 2**16
SOCKET = None
SOI = b'\xff\xd8'
EOI = b'\xff\xd9'

# -------------------------------- NETWORK ------------------------------------

_id = 0
def say(message = ""):
	global _id, SOCKET
	res_image = None
	res_text = None
	# connect
	if SOCKET == None:
		SOCKET = socket(AF_INET, SOCK_STREAM)
		SOCKET.connect((IP, PORT))
		#SOCKET.settimeout(None)
	# send message
	print("[OUT] %s" % repr(message))
	SOCKET.send((str(message)+"\n").encode())
	# receive response
	data = SOCKET.recv(BUFFER_SIZE)
	# process response
	if SOI in data:
		while data.find(EOI) == -1:
			data += SOCKET.recv(BUFFER_SIZE)
		image = data[data.find(SOI):data.find(EOI)+2]
		with open("img%s.jpg" % _id, "wb") as f:
			f.write(image)
		msg = "[IN] Image of %s bytes stored in img%s.jpg." % (len(image), _id)
		tail = data[data.find(EOI)+2:]
		if len(tail) > 2:
			res_text = tail.decode(errors = 'ignore')
			msg += " It also contained: '%s'." % res_text.strip()
			
		res_image = "img%s.jpg" % _id
	else:
		print("[IN] %s" % repr(data.decode()))
		res_text = data.decode()
	# return
	_id += 1
	return res_image, res_text

def notify():
	try:
		dummy = socket(AF_INET, SOCK_STREAM)
		dummy.setblocking(False)
		dummy.connect(('1.2.3.4', 80))
	except:
		pass

	#data = SOCKET.recv(BUFFER_SIZE)

# --------------------------------- IMAGE -------------------------------------

def show(img, name = "Image", scale = 5):
	#print(name)
	return
	cv.imshow(name, cv.resize(img, (0,0), fx = scale, fy = scale, interpolation = 0))
	cv.waitKey(0)
	cv.destroyAllWindows()

def trim_borders(img, white_threshold = 255):
	white_cols = [n for n,v in enumerate(np.mean(img, 0)) if np.mean(v) > white_threshold]
	img = np.delete(img, white_cols, 1)
	white_rows = [n for n,v in enumerate(np.mean(img, 1)) if np.mean(v) > white_threshold]  
	img = np.delete(img, white_rows, 0)
	return img

def fix_columns(img, blur_radius = 2, hor_threshold = 400, ver_threshold = 100, outlier_factor = 3):
	borders = np.mean(cv.Canny(cv.blur(img,tuple([blur_radius]*2)), hor_threshold, ver_threshold), 0)
	outliers_threshold = np.mean(borders) + outlier_factor*np.std(borders)
	cuts = [n for n in range(len(borders)) if borders[n] > outliers_threshold]
	cuts.append(len(borders))
	#print("Points to cut image: %s" % cuts)
	for n in range(len(cuts) - 1):
		if not n%2:
			img[:,cuts[n]:cuts[n+1]] = np.fliplr(img[:,cuts[n]:cuts[n+1]])
	return img

def match_coins(img, similarity_threshold = 10**7):
	coins = [1, 2, 5, 10, 20, 50, 100, 200]
	res = 0
	for coin in coins:
		template = cv.imread("./coins/%s.jpg" % coin)
		radius = len(template)
		comparison = cv.matchTemplate(img, template, cv.TM_SQDIFF)
		matches = [] 
		for r in range(len(comparison)):
			for c in range(len(comparison[r])):
				if comparison[r][c] < similarity_threshold and not any(sqrt((r2-r)**2 + (c2-c)**2) < radius/2 for r2, c2 in matches):
					matches.append((r,c))
		res += len(matches)*coin
	return res

def identify(img_path):
	# open image
	img = cv.imread(img_path)
	show(img, "Before")
	img = trim_borders(img)
	show(img, "After crop")
	# get column cuts
	img = fix_columns(img)
	show(img, "After column flips")
	# convolution to identify coins
	return match_coins(img)

# ---------------------------- MAIN -------------------------------------------

#"""
while True:
	notify()
	img, tail = say()
	if tail == None:
		say()
	amount = identify(img)
	say(amount)

	#sleep(1)
#"""
#print(identify("img9.jpg"))