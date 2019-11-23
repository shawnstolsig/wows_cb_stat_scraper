import requests
import time
import pandas as DataFrame
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pickle


def save_obj(obj, name ):
    ''' 
    '   A function for saving an object to a file using pickle
    '   Parameters: object and filename     Returns: none
    '''
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    ''' 
    '   A function for loading an object from a file using pickle
    '   Parameters: filename     Returns: object
    '''
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


driver = webdriver.Firefox()
driver.get("https://worldofwarships.com/")

# These steps aren't needed when walking through console
time.sleep(30)
print("sleep over")


url = 'http://clans.worldofwarships.com/clans/gateway/wows/clan-battles/history'

driver.get(url)
time.sleep(5)
print("second sleep over")

html = driver.execute_script("return document.documentElement.outerHTML")
sel_soup = BeautifulSoup(html, "html.parser")


# Things to scrape
# battle_summary = sel_soup.findAll("div", {"class": "Table__tr__1oPFL Table__isHovering__2s3cH"})
# battle_datetime = sel_soup.findAll("div", {"class": "Table__value__1GrFr"})  # index 0 for datetime
# session_id (might need to enter manually)
# ownteam_alpha_or_bravo (might need to enter manually)
# opponent_tag = sel_soup.findAll("span", {"class": "ClanTag__tag__1nUnl"})
# map_name = sel_soup.findAll("div", {"class": "Table__td__b2Kzr.Table__left__36pfA"}) # index 0 for map name
# enemy_ship_list = sel_soup.findAll("div", {"class": "BattleTeamsList__shipName__1QlOg"}) # either the last 8 indexes, or the odd indexes
# win_or_loss = sel_soup.findAll("div", {"class": "Table__td__b2Kzr.Table__center__28eHa"})  # will need to traverse this one a bit to sort out numbers vs the icons for struggle games.  negative numbers for losses, postive for wins

# table = sel_soup.findAll("div", {"class": "ClanBattlesTable__container__3udH"})
# battles = sel_soup.findAll("div", {"class": "Table__tr__1oPFL Table__isHovering__2s3cH"})
# datetimes_maps = sel_soup.findAll("div", {"class": "Table__value__1GrFr"})
# opponents = sel_soup.findAll("div", {"class": ClanTag__tag__1nUnl"})
# names = sel_soup.findAll("div", {"class": "BattleTeamsList__nickname__1nkU_"})
# ships = sel_soup.findAll("div", {"class": "BattleTeamsList__shipName__1QlOg"})

# struggle stuff
    # wins
    # demotion victory
    # <img alt="" src="//glossary-wows-global.gcdn.co/icons/clans/custom/misc/cvc_list_demotion_victory_0fffa5bbb5ff8d21243817ee632cfc208cefc38ec943c0174d7d02f78f5c4aca.png"/> ***************
    # <div class="ClanBattlesTable__victory__1DrFU ClanBattlesTable__numResult__17D8d">0</div>
    # promotion victory
    # <img alt="" src="//glossary-wows-global.gcdn.co/icons/clans/custom/misc/cvc_list_promotion_victory_0aa69f9b10965301e61dc9d2e5c62bb9706e12d57b134a636d7aca3703bc02cd.png"/> ****************************
    # <div class="ClanBattlesTable__victory__1DrFU ClanBattlesTable__numResult__17D8d">0</div>
    # promotion victory (START OF STRUGGLE)
    # <div class="ClanBattlesTable__arrowIcon__1EIWj ClanBattlesTable__promotion__biMm5"></div>
    # <div class="ClanBattlesTable__victory__1DrFU ClanBattlesTable__numResult__17D8d">1</div>    ## still positive result

    # defeat
    # defeat, start of struggle
    # <div class="ClanBattlesTable__arrowIcon__1EIWj ClanBattlesTable__demotion__3OTzE"></div>
    # <div class="ClanBattlesTable__defeat__3Jl6w ClanBattlesTable__numResult__17D8d">-4</div>
    # demotion defeat
    # <img alt="" src="//glossary-wows-global.gcdn.co/icons/clans/custom/misc/cvc_list_demotion_defeat_e3865a661dfdd2e435317841b36433cf8f9dc73534863ff5bdd3ff470f278e2b.png"/>  ************
    # <div class="ClanBattlesTable__defeat__3Jl6w ClanBattlesTable__numResult__17D8d">0</div>
    # promotion defeat
    # <img alt="" src="//glossary-wows-global.gcdn.co/icons/clans/custom/misc/cvc_list_promotion_defeat_cf85b2b782009e997bd48e818c35b4718a0cc38e12f2d6c2f7b0177ee9c1a042.png"/>  ************
    # <div class="ClanBattlesTable__defeat__3Jl6w ClanBattlesTable__numResult__17D8d">0</div>

# dataset:
data = []

# this returns list of five elements per battle: date/time, battle result, map, realm, and enemy clan tag/name
battle_high_level = sel_soup.findAll("div", {"class": "Table__value__1GrFr"})
rating = sel_soup.find("span", {"class": "ClanBattlesHistory__dropdownTeamLabel__1SKtb"}).text[0]
print(f"going to loop {int(len(battle_high_level)/5)} times")
for i in range(int(len(battle_high_level)/5)): 

    result = 'undefined'
    points_adjustment = 'undefined'

    # regular win
    if battle_high_level[i*5+1].div.div.find("div", {"class": "ClanBattlesTable__victory__1DrFU ClanBattlesTable__numResult__17D8d ClanBattlesTable__show__2Gw2G"}):
        result = 'W'
        points_adjustment = int(battle_high_level[i*5+1].div.div.find("div", {"class": "ClanBattlesTable__victory__1DrFU ClanBattlesTable__numResult__17D8d ClanBattlesTable__show__2Gw2G"}).text)
    # struggle win
    elif battle_high_level[i*5+1].div.div.find("div", {"class": "ClanBattlesTable__victory__1DrFU ClanBattlesTable__numResult__17D8d"}):
        result = 'W'
        points_adjustment = int(battle_high_level[i*5+1].div.div.find("div", {"class": "ClanBattlesTable__victory__1DrFU ClanBattlesTable__numResult__17D8d"}).text)
    # regular loss
    elif battle_high_level[i*5+1].div.div.find("div", {"class": "ClanBattlesTable__defeat__3Jl6w ClanBattlesTable__numResult__17D8d ClanBattlesTable__show__2Gw2G"}):
        result = "L"
        points_adjustment = int(battle_high_level[i*5+1].div.div.find("div", {"class": "ClanBattlesTable__defeat__3Jl6w ClanBattlesTable__numResult__17D8d ClanBattlesTable__show__2Gw2G"}).text)
    # struggle loss
    elif battle_high_level[i*5+1].div.div.find("div", {"class": "ClanBattlesTable__defeat__3Jl6w ClanBattlesTable__numResult__17D8d"}):
        result = "L"
        points_adjustment = int(battle_high_level[i*5+1].div.div.find("div", {"class": "ClanBattlesTable__defeat__3Jl6w ClanBattlesTable__numResult__17D8d"}).text)

    if points_adjustment == 0:
        points_adjustment = 'S'

    # print(battle_high_level[i*5].text, result, points_adjustment, battle_high_level[i*5+2].text, battle_high_level[i*5+4].find("span", {"class": "ClanTag__tag__1nUnl"}).text.replace('[','').replace(']',''))

    data.append(
        {   
            'rating played': rating,
            'date/time': battle_high_level[i*5].text,
            'result': result,
            'points adjustment': points_adjustment,
            'map': battle_high_level[i*5+2].text,
            'opponent': battle_high_level[i*5+4].find("span", {"class": "ClanTag__tag__1nUnl"}).text.replace('[','').replace(']','')
        }
    )

# print("10 sec flip to bravo rating")
# time.sleep(10)
# print("sleep over")

# # this returns list of five elements per battle: date/time, battle result, map, realm, and enemy clan tag/name
# battle_high_level = sel_soup.findAll("div", {"class": "Table__value__1uAVE"})
# rating = sel_soup.find("span", {"class": "ClanBattlesHistory__dropdownTeamLabel__1SKtb"}).text[0]
# print(f"going to loop {int(len(battle_high_level)/5)} times")
# for i in range(int(len(battle_high_level)/5)): 

#     result = 'undefined'
#     points_adjustment = 'undefined'

#     # regular win
#     if battle_high_level[i*5+1].div.div.find("div", {"class": "ClanBattlesTable__victory__1DrFU ClanBattlesTable__numResult__17D8d ClanBattlesTable__show__2Gw2G"}):
#         result = 'W'
#         points_adjustment = int(battle_high_level[i*5+1].div.div.find("div", {"class": "ClanBattlesTable__victory__1DrFU ClanBattlesTable__numResult__17D8d ClanBattlesTable__show__2Gw2G"}).text)
#     # struggle win
#     elif battle_high_level[i*5+1].div.div.find("div", {"class": "ClanBattlesTable__victory__1DrFU ClanBattlesTable__numResult__17D8d"}):
#         result = 'W'
#         points_adjustment = int(battle_high_level[i*5+1].div.div.find("div", {"class": "ClanBattlesTable__victory__1DrFU ClanBattlesTable__numResult__17D8d"}).text)
#     # regular loss
#     elif battle_high_level[i*5+1].div.div.find("div", {"class": "ClanBattlesTable__defeat__3Jl6w ClanBattlesTable__numResult__17D8d ClanBattlesTable__show__2Gw2G"}):
#         result = "L"
#         points_adjustment = int(battle_high_level[i*5+1].div.div.find("div", {"class": "ClanBattlesTable__defeat__3Jl6w ClanBattlesTable__numResult__17D8d ClanBattlesTable__show__2Gw2G"}).text)
#     # struggle loss
#     elif battle_high_level[i*5+1].div.div.find("div", {"class": "ClanBattlesTable__defeat__3Jl6w ClanBattlesTable__numResult__17D8d"}):
#         result = "L"
#         points_adjustment = int(battle_high_level[i*5+1].div.div.find("div", {"class": "ClanBattlesTable__defeat__3Jl6w ClanBattlesTable__numResult__17D8d"}).text)

#     if points_adjustment == 0:
#         points_adjustment = 'S'

#     # print(battle_high_level[i*5].text, result, points_adjustment, battle_high_level[i*5+2].text, battle_high_level[i*5+4].find("span", {"class": "ClanTag__tag__1nUnl"}).text.replace('[','').replace(']',''))

#     data.append(
#         {   
#             'rating played': rating,
#             'date/time': battle_high_level[i*5].text,
#             'result': result,
#             'points adjustment': points_adjustment,
#             'map': battle_high_level[i*5+2].text,
#             'opponent': battle_high_level[i*5+4].find("span", {"class": "ClanTag__tag__1nUnl"}).text.replace('[','').replace(']','')
#         }
#     )



print(data)
save_obj(data, "saved")

csv_string = ",,Date,Session,Clan,Rating,Opponent,#,Map,Notes,Ya,Mo,Oh,Kr,GK,Co,Th,Re,Bo,Za,DM,Sa,Hi,Go,He,Ve,Yo,PR,Mk,St,Wo,Sm,Mi,Co,Sh,Hg,Hy,Ge,So,Gr,Kh,52,Da,Kl,Ma,PE,YY,X,,486,Points\n"
for battle in data:
    csv_string += f",,{battle['date/time']},,KSD,{battle['rating played']},{battle['opponent']},,{battle['map']},,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,{battle['result']},{battle['points adjustment']}\n"


with open("ksd_alpha_scrape.csv", "w") as output:
    output.write(csv_string)