from threading import Thread
from time import sleep
from socket import socket, AF_INET, SOCK_STREAM
from re import compile

HOST = ('52.49.91.111', 2092)
MAX_BUFFER = 2**15
MSGS = compile(r'^ROUND (\d+): (\d+) -> (\w+) \{(.+?)\}( no_proposal)?( \(ROUND FINISHED\))?$').search
LEARN_ARGS = compile(r'servers: \[(.+?)\], secret_owner: (\d+)').search
PROMISE_ARGS = compile(r'(\d+),(\d+)').search
ACCEPT_ARGS = compile(r'id: \{(\d+),(\d+)\}, value: \{servers: \[(.+?)\], secret_owner: (\d+)\}').search
NUM_NODES = 7

class Node:
	connected = set()
	injected = set()

	def __init__(self, master):
		self.master = master
		self.socket = socket(AF_INET, SOCK_STREAM)
		self.socket.connect(HOST)
		self.server = None
		self.n = 1000
		self.state = 'idle'
		self.promises_received = 0
		self.accepted_received = 0
		self.quorum = None

	def say(self, msg='', parse=True):
		if self.master: print('=' * 83)
		if len(msg):
			if self.master: print('--- SENT %s\n%s' % ('-' * 74, msg.strip()))
			self.socket.send(msg.encode())
		ans = self.socket.recv(MAX_BUFFER).decode().strip()
		if len(ans) and self.master: print('--- RECEIVED %s\n%s' % ('-' * 70, ans))
		if ans.startswith('SERVER ID'):
			self.server = int(ans.rsplit(' ID: ', 1)[-1].split('\n', 1)[0])
			Node.connected.add(self.server)
		msgs = [MSGS(msg) for msg in ans.split('\n')]
		msgs = [msg.groups() for msg in msgs if msg is not None]
		res = []
		for rnd, src, cmd, args, no_prop, end in msgs:
			if cmd in ['LEARN', 'ACCEPTED']:
				args = LEARN_ARGS(args).groups()
				args = {
					'servers': list(map(int, args[0].split(','))),
					'secret_owner': int(args[1])
				}
			elif cmd == 'PROMISE':
				args = PROMISE_ARGS(args).groups()
				args = {
					'n': int(args[0]),
					'server': int(args[1])
				}
			elif cmd == 'PREPARE':
				self.socket.send(('PROMISE %s no_proposal -> %s\n' % (args, src)).encode())
			elif cmd == 'ACCEPT':
				n, server, servers, secret_owner = ACCEPT_ARGS(args).groups()
				self.socket.send(('ACCEPTED {servers: [%s], secret_owner: %s} no_proposal -> %s\n' % (servers, secret_owner, src)).encode())
			else:
				print('I don\'t know anything about %s' % cmd)
			res.append({
				'round': int(rnd),
				'src': int(src),
				'cmd': cmd,
				'args': args,
				'no_prop': no_prop is not None,
				'end': end is not None
			})
		return res

	def run(self):
		self.say()  # get server id
		while len(Node.connected) < NUM_NODES: sleep(.1)  # wait for every node to connect
		if self.master: print(Node.connected)
		next_msg = ''
		while True:
			sleep(.01)
			msgs = self.say(next_msg)
			next_msg = ''
			for msg in msgs:
				if msg['cmd'] == 'LEARN':
					self.quorum = [s for s in msg['args']['servers']]
					self.secret_owner = msg['args']['secret_owner']
					if self.server in self.quorum and self.master:
						self.state = 'prepare'
			if self.state == 'prepare':
				for dst in self.quorum:
					next_msg += 'PREPARE {%d,%d} -> %d\n' % (self.n, self.server, dst)
				self.promises_received = 0
				self.state = 'accept'
			elif self.state == 'accept':
				self.promises_received += len([
					m for m in msgs
					if m['cmd'] == 'PROMISE' and m['args']['n'] == self.n and m['args']['server'] == self.server
				])
				if self.promises_received == len(self.quorum):
					kick_members = [m for m in self.quorum if m not in Node.connected and m != self.secret_owner]
					add_members = [m for m in Node.connected if m not in self.quorum]
					if len([m for m in self.quorum if m in Node.connected]) / len(self.quorum) > .5:
						print("=== INJECTING ALTERATION: CHANGE KEY OWNER ===")
						new_quorum = self.quorum
						new_owner = self.server
					elif len(add_members):
						print("=== INJECTING ALTERATION: ADD MEMBER ===")
						new_quorum = self.quorum + [add_members[0]]
						new_owner = self.secret_owner
					elif len(kick_members) and len(self.quorum) > 3:
						print("=== INJECTING ALTERATION: KICK MEMBER ===")
						kick = kick_members[0]
						new_quorum = [m for m in self.quorum if m != kick]
						new_owner = self.secret_owner
					for dst in self.quorum:
						next_msg += 'ACCEPT {id: {%d,%d}, value: {servers: [%s], secret_owner: %d}} -> %d\n' % (
							self.n,
							self.server,
							','.join(map(str, new_quorum)),
							new_owner,
							dst
						)
					self.n += 1
					self.quorum = new_quorum
					self.secret_owner = new_owner
					self.accepted_received = 0
					self.state = 'idle'

if __name__ == '__main__':
	nodes = [Node(n == 0) for n in range(NUM_NODES)]
	threads = [Thread(target=node.run) for node in nodes]
	[t.start() for t in threads]
	[t.join() for t in threads]