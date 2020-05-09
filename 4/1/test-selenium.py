from selenium import webdriver
from time import sleep

USER = ("imbeciles", "imbeciles")
LOGIN_URL = "http://%s.elbruto.es/login" % USER[0]

fp = webdriver.FirefoxProfile()
fp.set_preference("plugin.state.flash", 2)
wd = webdriver.Firefox(fp)
wd.get(LOGIN_URL)
wd.find_element_by_name("pass").send_keys(USER[1])
wd.find_element_by_name("submit").click()
wd.implicitly_wait(0.2)
sleep(1)
wd.get("http://imbeciles.elbruto.es/vs/prrr")
wd.find_element_by_id("btn").click()