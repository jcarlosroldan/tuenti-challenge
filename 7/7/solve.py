from time import sleep
from selenium import webdriver

def solve(puzzle, clues):
	puzzle = puzzle.replace(' ','')            
	length = puzzle.index('\n')+1
	letters = [(letter, divmod(index, length)) for index, letter in enumerate(puzzle)]
	lines = {}
	offsets = {(1, 0):0, (1, -1):-1, (1, 1):1}
	for direction, offset in offsets.items():
		lines[direction] = []
		for i in range(length):
			for j in range(i, len(letters), length + offset):
				lines[direction].append(letters[j])
			lines[direction].append('\n')
	lines[(0, 1)]  = letters
	lines[(0, -1)] = [i for i in reversed(letters)]
	lines[(-1, 0)] = [i for i in reversed(lines[(1, 0)])]
	lines[(-1, 1)] = [i for i in reversed(lines[(1, -1)])]
	lines[(-1, -1)] = [i for i in reversed(lines[(1, 1)])]
	for direction, tup in lines.items():
		string = ''.join([i[0] for i in tup])
		for word in clues:
			if word in string:
				location = tup[string.index(word)][1]
				yield (location[0], location[1], location[0]+(len(word)-1)*direction[0], location[1]+(len(word)-1)*direction[1])

wd = webdriver.Firefox()
wd.get("http://52.49.91.111:8036/word-soup-challenge")

while True:
	wd.implicitly_wait(1.5)
	sleep(0.2)
	puzzle = wd.find_elements_by_css_selector("#container table")[0].text
	clues = [e.text for e in wd.find_elements_by_css_selector("#words div") if e.get_attribute("id").startswith("word-")]
	for r0, c0, r1, c1 in solve(puzzle, clues):
		wd.find_elements_by_css_selector("#container table tr:nth-child(%s) td:nth-child(%s)" % (r0+1, c0+1))[0].click()
		wd.implicitly_wait(0.3)
		sleep(0.2)
		wd.find_elements_by_css_selector("#container table tr:nth-child(%s) td:nth-child(%s)" % (r1+1, c1+1))[0].click()
		wd.implicitly_wait(0.3)
		sleep(0.2)
	wd.implicitly_wait(2)
	sleep(0.2)
	wd.find_elements_by_css_selector("button")[0].click()