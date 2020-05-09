from requests import get, Session
from selenium import webdriver

URI = "https://52.49.91.111:8443/ghost"

prof = webdriver.FirefoxProfile()
prof.accept_untrusted_certs = True
wd = webdriver.Firefox(firefox_profile = prof)

nv = ""
v = ""

while True:
	wd.get(URI)
	nv = wd.find_element_by_tag_name("pre").text
	if len(nv) > len(v) or v == "":
		v = nv
	else:
		break
wd.close()

with open("result.html", "w") as f:
	f.write('<!doctype html><html><body><img src="data:image/png;base64,%s"></body></html>' % v.replace("\n",""))