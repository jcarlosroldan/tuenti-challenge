# Tuenti Challenge Edition 6 Level 8
from socket import socket, AF_INET, SOCK_STREAM
from numpy import array


sock = socket(AF_INET, SOCK_STREAM)

def read(msg = None):
	if msg != None:
		sock.send(str.encode(msg))
	return sock.recv(1024).decode()

sock.connect(("52.49.91.111",1986,))
replacement = {"#":1," ":0,"x":0}
lab = array([[replacement[c] for c in line] for line in read().split("\n")[:-1]])
print(lab)
while True:
	print(lab)
	lab = read(equiv[input("> ")]+"\n")