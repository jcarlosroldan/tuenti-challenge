from socket import socket, AF_INET, SOCK_STREAM
from re import compile

HOST = ('52.49.91.111', 2092)
MAX_BUFFER = 2**15
POOL_SIZE = 10

pool = [socket(AF_INET, SOCK_STREAM) for _ in range(POOL_SIZE)]
[socket.connect(HOST) for socket in pool]

while True:
	for s, socket in enumerate(pool, 1):
		msg = ''#input('(%d) >>> ' % s).strip()
		if len(msg):
			msg = msg + '\n'
			socket.send(msg.encode())
		ans = socket.recv(MAX_BUFFER).decode()
		print(ans)

# PREPARE {1000, 9} -> 1
# ACCEPT {id: {4, 5}, value: {servers: [1,2,3,4,5,6,7,8], secret_owner: 4}}