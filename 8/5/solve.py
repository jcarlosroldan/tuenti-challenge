from re import search
from socket import socket, AF_INET, SOCK_STREAM

# Tuenti Challenge Edition 8 Level 1

PROBLEM_SIZE = "submit"
HOST = ("52.49.91.111", 3241)
NEXT = b""

# -- problem specific functions --------------------------------------------- #

_socket = None
def init():
	global _socket
	_socket = socket(AF_INET, SOCK_STREAM)
	_socket.connect(HOST)

def tell(message):
	#print("[Telling '%s']" % message.decode())
	_socket.send(message)
	res = _socket.recv(1000).decode().strip()
	print(res)
	if res[0] == ">" and "key is" in res:
		with open("%s.out" % PROBLEM_SIZE.lower(), "w") as fp:
			fp.write(search('"(.+?)"', res).group(1))
		exit()
	return res

def run():
	init()
	tell((PROBLEM_SIZE.upper() + "\n").encode())
	while True:
		chains = tell(NEXT).split("\n")[-1].split(" ")
		tell(solve(chains).encode() + b"\n")

_chains = None
def solve(chains):
	global _chains
	_chains = chains
	N = len(chains)
	return ",".join(map(str, reconstruct("", "", [])))

def reconstruct(seq1, seq2, used):
	shortest = min([seq1, seq2], key = len)
	longest = max([seq1, seq2], key = len)
	tail = longest[len(shortest):]
	for n, chain in enumerate(_chains):
		if n not in used and (chain.startswith(tail) or tail.startswith(chain)):
			res = reconstruct(shortest + chain, longest, used + [n])
			if res != None: return res
	if len(shortest) == len(longest) != 0:
		return list(sorted(u + 1 for u in used))

# -- entrypoint ------------------------------------------------------------- #

if __name__ == "__main__":
	run()