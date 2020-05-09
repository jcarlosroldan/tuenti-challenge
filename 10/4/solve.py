from requests import get

URL = 'http://steam-origin.contest.tuenti.net:9876/games/cat_fight/get_key'
HEADERS = {'Host': 'pre.steam-origin.contest.tuenti.net:9876'}

data = get(URL, headers=HEADERS).json()
with open('key.txt', 'w') as fp:
	fp.write(data['key'])