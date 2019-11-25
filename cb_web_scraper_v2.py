import requests
import urllib3
import json
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
# from selenium.webdriver.firefox.webdriver import FirefoxProfile
# from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
import pickle

# # # open Firefox (with Selenium)
# driver = webdriver.Firefox()
# driver.get("https://worldofwarships.com/")

# # # wait until user to login (later, replace this with homebrew OpenID connection)
# input("Press enter once logged into WG...")

# # # once user is logge in the browser, 
# driver.get('https://clans.worldofwarships.com/clans/wows/ladder/api/battles/?team=1')

# input("Save file in same folder, using 'data1' for alpha.  Press enter when done.")

# driver.get('https://clans.worldofwarships.com/clans/wows/ladder/api/battles/?team=2')

# input("Save file in same folder, using 'data2' for bravo.  Press enter when done. ")

# some variables we'll need later
# create string for writing to CSV
csv_string = "Date,Session,Clan,Rating,Opponent,#,Map,Notes,Ya,Mo,Oh,Kr,GK,Co,Th,Re,Bo,Za,DM,Sa,Hi,Go,He,Ve,Yo,PR,Mk,St,Wo,Sm,Mi,Co,Sh,Hg,Hy,Ge,So,Gr,Kh,52,Da,Kl,Ma,PE,YY,X,,486,Points\n"
# create dictionary for ship indexes:
ship_index_table = {
    'Yamato': 10,
    'Montana': 11,
    'Ohio': 12,
    'Kremlin': 13,
    'Großer Kurfürst': 14, 
    'Conqueror': 15,
    'Thunderer': 16,
    'République': 17, 
    'Bourgogne': 18,
    'Zaō': 19,
    'Des Moines': 20,
    'Salem': 21,
    'Hindenburg': 22,
    'Goliath': 23,
    'Henri IV': 24,
    'Venezia': 25,
    'Yoshino': 26,
    'Puerto Rico': 27,
    'Moskva': 28,
    'Stalingrad': 29,
    'Worcester': 30,
    'Smolensk': 31,
    'Minotaur': 32,
    'Colbert': 33,
    'Shimakaze': 34,
    'Harugumo': 35,
    'Hayate': 36,
    'Gearing': 37,
    'Somers': 38,
    'Grozovoi': 39,
    'Khabarovsk': 40,
    'Z-52': 41,
    'Daring': 42,
    'Kléber': 43,    
    'Marceau': 44,
    'Paolo Emilio': 45,
    'Yueyang': 46
}

# FOR ALPHA
# save file as "data.json"
try: 
    with open("data1.json", encoding="utf8") as json_file:
        data = json.load(json_file)
except: 
    print("Couldn't find/open data1.json")
    exit()

for i in range(len(data)):

    # get data from JSON
    date_time = data[i]['finished_at'] 
    own_clan_tag = data[i]['teams'][0]['claninfo']['tag']
    own_clan_rating = data[i]['teams'][0]['team_number']
    opponent_tag = data[i]['teams'][1]['claninfo']['tag']
    rating_delta = data[i]['teams'][0]['rating_delta']
    map_name = data[i]['map']['name']
    result = data[i]['teams'][0]['result']

    # convert date
    date_time = date_time[5:10]

    # convert json result to "L" or "W"
    if result == "defeat":
        result = "L"
    elif result == "victory":
        result = "W"

    # convert team number to 'A' or "B"
    if own_clan_rating == 1:
        own_clan_rating = 'A'
    elif own_clan_rating == 2:
        own_clan_rating = 'B'

    # create list of zeros to help track counts.  abbreviateint "sl" for "ship_list"
    sl = []
    for k in range(len(ship_index_table) + 8):
        sl.append(0)

    # record enemy ships
    for j in range(len(data[i]['teams'][1]['players'])):

        # get ship string
        this_ship = data[i]['teams'][1]['players'][j]['ship']['name']

        # strip off rental ship brackets
        this_ship = this_ship.replace('[','').replace(']','')
    
        sl[ship_index_table[data[i]['teams'][1]['players'][j]['ship']['name']]] += 1

    # remove zeroes
    for x in range(len(sl)):
        if sl[x] == 0:
            sl[x] = ''


    # add battle as line in csv string
    csv_string += f"{date_time},,{own_clan_tag},{own_clan_rating},{opponent_tag},,{map_name},,{sl[0]},{sl[1]},{sl[2]},{sl[3]},{sl[4]},{sl[5]},{sl[6]},{sl[7]},{sl[8]},{sl[9]},{sl[10]},{sl[11]},{sl[12]},{sl[13]},{sl[14]},{sl[15]},{sl[16]},{sl[17]},{sl[18]},{sl[19]},{sl[20]},{sl[21]},{sl[22]},{sl[23]},{sl[24]},{sl[25]},{sl[26]},{sl[27]},{sl[28]},{sl[29]},{sl[30]},{sl[31]},{sl[32]},{sl[33]},{sl[34]},{sl[35]},{sl[36]},{sl[37]},,{result},{rating_delta}\n"


# FOR BRAVO
try: 
    with open("data2.json", encoding="utf8") as json_file:
        data = json.load(json_file)
except: 
    print("Couldn't find/open data2.json")
    exit()

for i in range(len(data)):

    # get data from JSON
    date_time = data[i]['finished_at'] 
    own_clan_tag = data[i]['teams'][0]['claninfo']['tag']
    own_clan_rating = data[i]['teams'][0]['team_number']
    opponent_tag = data[i]['teams'][1]['claninfo']['tag']
    rating_delta = data[i]['teams'][0]['rating_delta']
    map_name = data[i]['map']['name']
    result = data[i]['teams'][0]['result']

    # convert date
    date_time = date_time[5:10]

    # convert json result to "L" or "W"
    if result == "defeat":
        result = "L"
    elif result == "victory":
        result = "W"

    # convert team number to 'A' or "B"
    if own_clan_rating == 1:
        own_clan_rating = 'A'
    elif own_clan_rating == 2:
        own_clan_rating = 'B'

    # create list of zeros to help track counts.  abbreviateint "sl" for "ship_list"
    sl = []
    for k in range(len(ship_index_table) + 8):
        sl.append(0)

    # record enemy ships
    for j in range(len(data[i]['teams'][1]['players'])):

        # get ship string
        this_ship = data[i]['teams'][1]['players'][j]['ship']['name']

        # strip off rental ship brackets
        this_ship = this_ship.replace('[','').replace(']','')
        
        print(f"j is {j} and ship is {this_ship}")
        sl[ship_index_table[this_ship]] += 1

    # remove zeroes
    for x in range(len(sl)):
        if sl[x] == 0:
            sl[x] = ''


    # add battle as line in csv string
    csv_string += f"{date_time},,{own_clan_tag},{own_clan_rating},{opponent_tag},,{map_name},,{sl[0]},{sl[1]},{sl[2]},{sl[3]},{sl[4]},{sl[5]},{sl[6]},{sl[7]},{sl[8]},{sl[9]},{sl[10]},{sl[11]},{sl[12]},{sl[13]},{sl[14]},{sl[15]},{sl[16]},{sl[17]},{sl[18]},{sl[19]},{sl[20]},{sl[21]},{sl[22]},{sl[23]},{sl[24]},{sl[25]},{sl[26]},{sl[27]},{sl[28]},{sl[29]},{sl[30]},{sl[31]},{sl[32]},{sl[33]},{sl[34]},{sl[35]},{sl[36]},{sl[37]},,{result},{rating_delta}\n"





with open("clan_battles_results.csv", "w") as output:
    output.write(csv_string)





# maybe pandas later?
# convert json to dataframe
# battles = pd.DataFrame(data)
# drop some unneeded columns
# df = df.drop(['realm', 'cluster_id', 'map_id', 'season_number', 'id'], axis=1)
# print(df.head())
