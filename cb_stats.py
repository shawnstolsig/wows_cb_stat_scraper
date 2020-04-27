'''
'   Purpose of this script is to convert json files containing clan battle results into a csv spreadsheet. 
'   When executed, the script will read any json files contained in the same directory as this file, 
'   store all battles as objects, convert each battle object to a comma seperated string, and finally output to a 
'   csv file called "clan_battle_results.csv."  The script will prevent duplicate battles (based of the battle ID 
'   assigned by WG) so any number of json files can be processed at once.  
'   
'   The input JSON files can be obtained at the following URLs, after you authenticate on the World of Warships website:
'   Alpha Rating (team 1): https://clans.worldofwarships.com/clans/wows/ladder/api/battles/?team=1
'   Bravo Rating (team 2): https://clans.worldofwarships.com/clans/wows/ladder/api/battles/?team=2
'
'   The format of the csv output is based on torino2dc's KSD/KSC/KSE Clan Wars Google sheet.  
'
'   To maintain, this file will need to be updated with new ships and date/session pairs before each season.
'   The global variables SESSION_IDS, SHIP_INDEX_TABLE, and CSV_STRING are the only things that need to be updated.
'
'   The script is current configured for Season 9.  This means tier X ships with dates/sessions ranging from 
'   April 15, 2020 to June 7, 2020.
'
'   Issues/future ideas: 
'   1. Read in ships and session id/date pairs from file so that this code does not need to be modified between seasons.
'   2. Even better...read in ships/clan battle season info from WG's API instead of external file.
'   3. Rather than relying on torino2dc's template, create a more generic output that could be used by other clans.
'
'''

import json
import os
import pytz
from datetime import datetime, timezone

#########################      global vars      ##########################################
# update session ids for each new season
SESSION_IDS = {
    '15/4': '1.1',
    '16/4': '1.2',
    '18/4': '1.3',
    '19/4': '1.4',
    '22/4': '2.1',
    '23/4': '2.2',
    '25/4': '2.3',
    '26/4': '2.4',
    '29/4': '3.1',
    '30/4': '3.2',
    '2/5': '3.3',
    '3/5': '3.4',
    '6/5': '4.1',
    '7/5': '4.2',
    '9/5': '4.3',
    '10/5': '4.4',
    '13/5': '5.1',
    '14/5': '5.2',
    '16/5': '5.3',
    '17/5': '5.4',
    '20/5': '6.1',
    '21/5': '6.2',
    '23/5': '6.3',
    '24/5': '6.4',
    '27/5': '7.1',
    '28/5': '7.2',
    '30/5': '7.3',
    '31/5': '7.4',
    '3/6': '8.1',
    '4/6': '8.2',
    '6/6': '8.3',
    '7/6': '8.4',
}

# update both SHIP_INDEX_TABLE and CSV_STRING whenever new ships added
SHIP_INDEX_TABLE = {
    'Yamato': 0,
    'Shikishima': 1,
    'Montana': 2,
    'Ohio': 3,
    'Kremlin': 4,
    'Großer Kurfürst': 5, 
    'Conqueror': 6,
    'Thunderer': 7,
    'République': 8, 
    'Bourgogne': 9,
    'Zaō': 10,
    'Des Moines': 11,
    'Salem': 12,
    'Hindenburg': 13,
    'Goliath': 14,
    'Henri IV': 15,
    'Venezia': 16,
    'Yoshino': 17,
    'Puerto Rico': 18,
    'Petropavlovsk': 19,
    'Moskva': 20,
    'Stalingrad': 21,
    'Worcester': 22,
    'Alexander Nevsky': 23,
    'Smolensk': 24,
    'Minotaur': 25,
    'Colbert': 26,
    'Shimakaze': 27,
    'Harugumo': 28,
    'Hayate': 29,
    'Gearing': 30,
    'Somers': 31,
    'Grozovoi': 32,
    'Khabarovsk': 33,
    'Z-52': 34,
    'Daring': 35,
    'Kléber': 36,    
    'Marceau': 37,
    'Paolo Emilio': 38,
    'Halland': 39,
    'Småland': 40,
    'Yueyang': 41,
    'Hakuryū': 42,
    'Midway': 43,
    'F.D. Roosevelt': 44,
    'Manfred von Richthofen': 45,
    'Audacious': 46,
}
CSV_STRING = "Date,Session,Clan,Rating,Opponent,#,Map,Players,Notes,Ya,Sk,Mo,Oh,Kr,GK,Co,Th,Re,Bo,Za,DM,Sa,Hi,Go,He,Ve,Yo,PR,Pp,Mk,St,Wo,Nv,Sm,Mi,Co,Sh,Hg,Hy,Ge,So,Gr,Kh,52,Da,Kl,Ma,PE,Hd,Sd,YY,Hk,Md,FR,MR,Au,X,,0,Points\n"


#########################      functions      ############################################
# get a list of all json files in working directory
def get_json_files():
    '''
    '   Returns a list of json filenames in the current directory. 
    '   Arguments: none    Return: list of strings
    '''

    # get current working directory
    location = os.getcwd()

    # declare empty list
    json_files = []

    # for each file in current directory
    for file in os.listdir(location):
        try: 
            # append to file list if it's a json file
            if file.endswith(".json"):
                json_files.append(str(file))
        # edge case: no json files found
        except Exception as e: 
            print("No files found")
            raise e

    print(f"Loading data from {len(json_files)} json files.")
    return json_files

# given a list of json files, return an unordered list of unique battle dictionaries
def load_battle_data(json_files):
    '''
    '   Generate an unordered list of unique battle objects(dictionaries) based off json files.
    '   Arguments: a list of strings representing json filenames   Return: Unordered list of battle objects
    '''

    # create empty lists
    battle_id_list = []
    unordered_battle_list = []

    # create counter for console message
    battle_counter = 0

    # loop through all json files
    for json_file in json_files:

        # try to open file and process input.  
        try: 
            with open(json_file, encoding="utf8") as j:
                data = json.load(j)

            # loop through json data and push only battles that don't currently exist...prevent duplicates
            for battle in data:

                # total battle counter...represents all battles in the input json files
                battle_counter += 1

                # if battle not already in battle list, update lists
                if battle['id'] not in battle_id_list:
                    unordered_battle_list.append(battle)
                    battle_id_list.append(battle['id'])

        # print error message if unable to open file
        except: 
            print(f"Couldn't find/open {json_file}")
    
    print(f'Total battles: {battle_counter}')
    print(f'Duplicate battles: {battle_counter-len(unordered_battle_list)}')
    print(f'Unique battles: {len(unordered_battle_list)}')
    return unordered_battle_list

# given a battle object, update the string to be written as a csv
def translate_battle_data(battle, csv_string):
    '''
    '   Converts battle object to a single row to be later written to a CSV
    '   Arguments: battle object and string to be printed to csv    Return: updated comma seperated string with battle data appended
    '''

    # get data from JSON
    date_time_iso = battle['finished_at'] 
    own_clan_tag = battle['teams'][0]['claninfo']['tag']
    own_clan_rating = battle['teams'][0]['team_number']
    opponent_tag = battle['teams'][1]['claninfo']['tag']
    rating_delta = battle['teams'][0]['rating_delta']
    map_name = battle['map']['name']
    result = battle['teams'][0]['result']

    # convert date from UTC timestamp to "DD/MM" format.  uses datetime and pytz libraries.
    date_time_obj_utc = datetime.fromisoformat(date_time_iso)
    date_time_obj_local = date_time_obj_utc.astimezone(pytz.timezone('US/Eastern'))
    date_time = f'{date_time_obj_local.day}/{date_time_obj_local.month}'

    # convert 0 point battles to "S" for struggle
    if rating_delta == 0:
        rating_delta = 'S'

    # convert json result to "L" or "W"
    if result == "defeat":
        result = "L"
    elif result == "victory":
        result = "W"

    # convert team number to 'A' or "B" ("team number" represents alpha or bravo rating)
    if own_clan_rating == 1:
        own_clan_rating = 'A'
    elif own_clan_rating == 2:
        own_clan_rating = 'B'

    # create player string
    player_string = ''
    for player in battle['teams'][0]['players']:
        player_string += f"{player['name']} "

    # create list of zeros to help track counts. 
    ship_counts = []
    for k in range(len(SHIP_INDEX_TABLE)):
        ship_counts.append(0)

    # record enemy ships
    for j in range(len(battle['teams'][1]['players'])):

        # get ship name string
        this_ship = battle['teams'][1]['players'][j]['ship']['name']

        # strip off rental ship brackets...rental ships and tech tree ships counted the same
        this_ship = this_ship.strip('[]')

        # increment count of current ship
        ship_counts[SHIP_INDEX_TABLE[this_ship]] += 1

    # remove zeroes from ship_count list 
    for x in range(len(ship_counts)):
        if ship_counts[x] == 0:
            ship_counts[x] = ''

    # add battle as line in csv string
    csv_string += f"{date_time},{SESSION_IDS[date_time]},{own_clan_tag},{own_clan_rating},{opponent_tag},(formula),{map_name},{player_string},script,"
    for ship in ship_counts:
            csv_string += f'{ship},'
    csv_string += f",,{result},{rating_delta}\n"

    return csv_string

# write csv_string to csv file
def write_string_to_csv(input_string):
    '''
    '   Write the csv string built by the script to a csv file
    '   Arguments: comma seperated string      Returns: none (but csv is written to cwd)
    '''

    print("Writing to clan_battles_results.csv...")

    with open("clan_battles_results.csv", "w") as output:
        output.write(input_string)


#########################      main      #################################################
print("Script starting...")

# create list of battle objects, taking in cwd json filenames
battle_list = load_battle_data(get_json_files())

# sort battle list by time battle finished (so most recent will be at bottom of csv)
battle_list = sorted(battle_list, key = lambda b: b['finished_at'] )

# convert battle objects into csv string.  note that csv_string is overwritten each loop.  
for battle in battle_list:
    CSV_STRING = translate_battle_data(battle, CSV_STRING)

# write csv string to csv file
write_string_to_csv(CSV_STRING)

print("Finished.")
