import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
# profile = FirefoxProfile(r"C:\Users\shawn\AppData\Local\Mozilla\Firefox\Profiles\yvtt5opx.selProfile")
# driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary, executable_path=r"C:\Users\shawn\AppData\Local\Programs\Python\Python38-32\geckodriver.exe")

driver = webdriver.Firefox()
driver.get("https://worldofwarships.com/auth/oid/new/")

time.sleep(40)
print("sleep over")
driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')

url = 'http://clans.worldofwarships.com/clans/gateway/wows/clan-battles/history'

# profile = webdriver.FirefoxProfile(r"C:\Users\shawn\AppData\Local\Mozilla\Firefox\Profiles\yvtt5opx.selProfile")
# web_soup = BeautifulSoup(web_r.text, 'html.parser')

# print(web_soup.findAll('img'))

driver.get(url)

# table = sel_soup.findAll("div", {"class": "ClanBattlesTable__container__3udH"})
# battles = sel_soup.findAll("div", {"class": "Table__tr__1oPFL Table__isHovering__2s3cH"})
# datetimes_maps = sel_soup.findAll("div", {"class": "Table__value__1GrFr"})
# opponents = sel_soup.findAll("div", {"class": ClanTag__tag__1nUnl"})
# names = sel_soup.findAll("div", {"class": "BattleTeamsList__nickname__1nkU_"})
# ships = sel_soup.findAll("div", {"class": "BattleTeamsList__shipName__1QlOg"})

html = driver.execute_script("return document.documentElement.outerHTML")
sel_soup = BeautifulSoup(html, "html.parser")
print(sel_soup.findAll("class=ClanBattlesHistory__teamText__2E-bw"))
