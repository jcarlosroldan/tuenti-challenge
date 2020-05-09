from requests import get
from bs4 import BeautifulSoup as soup
from urllib.parse import urljoin, urlparse
from time import sleep
from os import makedirs
from os.path import join, dirname

seed = 'http://52.49.91.111:8327/'

def scrap(base, download_path='site/'):
	sleep(.5)  # be nice
	visited = []
	to_visit = [base]
	while len(to_visit):
		url = to_visit.pop()
		visited.append(url)
		print(url)
		page = get(url, params={'goodboy': ''}).text
		if page.startswith('<html>'):
			links = [a['href'] for a in soup(page, 'html.parser').select('a')]
			links = [urljoin(url, lk) for lk in links]
			links = [lk for lk in links if lk not in visited and lk not in to_visit]
			to_visit.extend(links)
		else:
			path = join(download_path, urlparse(url).path.lstrip('/'))
			makedirs(dirname(path), exist_ok=True)
			with open(path, 'w', encoding='utf-8') as fp:
				fp.write(page)

scrap(seed)