# Tuenti Challenge Edition 6 Level 5
from socket import socket, AF_INET, SOCK_STREAM
from re import match, search

class Player:
	""" This is the Player IA """

	def __init__(self, path):
		self.load_words(path)
		self.connect()

	def load_words(self, path):
		""" Load words file as dictionary """
		with open(path,"r") as f:
			words = f.read().split("\n")
		self.words = {}
		for word in words:
			l = len(word)
			if not l in self.words:
				self.words[l] = []
			self.words[l].append(word)

	def connect(self):
		""" Connect to Tuenti socket """
		self.sck = socket(AF_INET, SOCK_STREAM)
		self.sck.connect(("52.49.91.111",9988,))
		self.read()

	def solve(self):
		""" Try to solve all the levels! """
		while True:
			try:
				self.level()
			except:
				break

	def level(self):
		""" Try to resolve one level. Returns True if done, False if failed """
		n = len(self.ask("\n"))
		words = self.words[n]
		letters = list("-ABCDEFGHIJKLMNOPQRSTUVWXYZ")
		pattern = "."*n
		fails = 0
		while fails < 6:
			s = self.best_separator(words,letters)
			letters.remove(s)
			new_pattern = self.ask(s)
			if new_pattern == None:
				return True
			elif new_pattern == pattern:
				fails += 1
				words = [w for w in words if s not in w]
			else:
				words = [w for w in words if match(new_pattern,w)!=None]
			pattern = new_pattern
			if len(words) < 100:
				possible = set("".join(words))
				letters = [l for l in letters if l in possible]
		return False

	def best_separator(self, words, letters):
		""" Get the best separator as the letter which bisects more the words """
		amount = []
		for letter in letters:
			amount.append(sum(letter in word for word in words))
		half = int(0.5*len(words))
		score = [abs(half-a) for a in amount]
		m = score.index(min(score))
		return letters[m]

	def read(self):
		""" Read response """
		return self.sck.recv(1024)

	def ask(self, msg):
		""" Send letter and get response """
		self.sck.send(str.encode(msg))
		resp = self.sck.recv(1024).decode()
		found = "key is: " in resp
		if found:
			print(search("key is: (\w+)\n", resp).group(1))
		else:
			if not "ready" in resp:
				return resp.split("\n\n")[2][::2].replace("_",".")


# try about 10 times
for _ in range(10):
	p = Player("words.txt")
	p.solve()