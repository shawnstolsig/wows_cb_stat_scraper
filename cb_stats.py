import json
import os
from datetime import datetime, timedelta

# update session ids for each new season
SESSION_IDS = {
    '22/1': '1.1',
    '23/1': '1.2',
    '25/1': '1.3',
    '26/1': '1.4',
    '29/1': '2.1',
    '30/1': '2.2',
    '1/2': '2.3',
    '2/2': '2.4',
    '5/2': '3.1',
    '6/2': '3.2',
    '8/2': '3.3',
    '9/2': '3.4',
    '12/2': '4.1',
    '13/2': '4.2',
    '15/2': '4.3',
    '16/2': '4.4',
    '19/2': '5.1',
    '20/2': '5.2',
    '22/2': '5.3',
    '23/2': '5.4',
    '26/2': '6.1',
    '27/2': '6.2',
    '29/2': '6.3',
    '1/3': '6.4',
    '4/3': '7.1',
    '5/3': '7.2',
    '7/3': '7.3',
    '8/3': '7.4',
}

# update both SHIP_INDEX_TABLE and csv_string headers whenever new ships added
SHIP_INDEX_TABLE = {
    'Yamato': 0,
    'Montana': 1,
    'Ohio': 2,
    'Kremlin': 3,
    'Großer Kurfürst': 4, 
    'Conqueror': 5,
    'Thunderer': 6,
    'République': 7, 
    'Bourgogne': 8,
    'Zaō': 9,
    'Des Moines': 10,
    'Salem': 11,
    'Hindenburg': 12,
    'Goliath': 13,
    'Henri IV': 14,
    'Venezia': 15,
    'Yoshino': 16,
    'Puerto Rico': 17,
    'Moskva': 18,
    'Stalingrad': 19,
    'Worcester': 20,
    'Smolensk': 21,
    'Minotaur': 22,
    'Colbert': 23,
    'Shimakaze': 24,
    'Harugumo': 25,
    'Hayate': 26,
    'Gearing': 27,
    'Somers': 28,
    'Grozovoi': 29,
    'Khabarovsk': 30,
    'Z-52': 31,
    'Daring': 32,
    'Kléber': 33,    
    'Marceau': 34,
    'Paolo Emilio': 35,
    'Yueyang': 36
}
CSV_STRING = "Date,Session,Clan,Rating,Opponent,#,Map,Notes,Ya,Mo,Oh,Kr,GK,Co,Th,Re,Bo,Za,DM,Sa,Hi,Go,He,Ve,Yo,PR,Mk,St,Wo,Sm,Mi,Co,Sh,Hg,Hy,Ge,So,Gr,Kh,52,Da,Kl,Ma,PE,YY,X,,0,Points\n"

# get a list of all json files in working directory
def get_json_files():
    location = os.getcwd()
    json_files = []

    for file in os.listdir(location):
        try: 
            if file.endswith(".json"):
                json_files.append(str(file))
        except Exception as e: 
            raise e
            print("No files found")

    print(f"Loading data from {len(json_files)} json files.")
    return json_files

# given a list of json files, return an unordered list of unique battle dictionaries
def load_battle_data(json_files):
    battle_id_list = []
    unordered_battle_list = []
    battle_counter = 0

    # loop through all data##.json files, where ## is 1 to 99
    for json_file in json_files:

        # try to open file and process input.  
        try: 
            with open(json_file, encoding="utf8") as j:
                data = json.load(j)

            # loop through json data and push only battles that don't currently exist...prevent duplicates
            for battle in data:
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

    # get data from JSON
    date_time_iso = battle['finished_at'] 
    own_clan_tag = battle['teams'][0]['claninfo']['tag']
    own_clan_rating = battle['teams'][0]['team_number']
    opponent_tag = battle['teams'][1]['claninfo']['tag']
    rating_delta = battle['teams'][0]['rating_delta']
    map_name = battle['map']['name']
    result = battle['teams'][0]['result']

    # convert date....NEED TO FIX THE DAY/TIMEZONE
    date_time_obj_utc = datetime.fromisoformat(date_time_iso)
    date_time_obj_local = date_time_obj_utc - timedelta(days=1)
    date_time = f'{date_time_obj_local.day}/{date_time_obj_local.month}'

    # convert 0 point battles to "S" for struggle
    if rating_delta == 0:
        rating_delta = 'S'

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
    for k in range(len(SHIP_INDEX_TABLE)):
        sl.append(0)

    # record enemy ships
    for j in range(len(battle['teams'][1]['players'])):

        # get ship string
        this_ship = battle['teams'][1]['players'][j]['ship']['name']

        # strip off rental ship brackets
        this_ship = this_ship.strip('[]')
        sl[SHIP_INDEX_TABLE[this_ship]] += 1

    # remove zeroes
    for x in range(len(sl)):
        if sl[x] == 0:
            sl[x] = ''

    # add battle as line in csv string
    csv_string += f"{date_time},{SESSION_IDS[date_time]},{own_clan_tag},{own_clan_rating},{opponent_tag},manbear67's script,{map_name},,{sl[0]},{sl[1]},{sl[2]},{sl[3]},{sl[4]},{sl[5]},{sl[6]},{sl[7]},{sl[8]},{sl[9]},{sl[10]},{sl[11]},{sl[12]},{sl[13]},{sl[14]},{sl[15]},{sl[16]},{sl[17]},{sl[18]},{sl[19]},{sl[20]},{sl[21]},{sl[22]},{sl[23]},{sl[24]},{sl[25]},{sl[26]},{sl[27]},{sl[28]},{sl[29]},{sl[30]},{sl[31]},{sl[32]},{sl[33]},{sl[34]},{sl[35]},{sl[36]},,,{result},{rating_delta}\n"

    return csv_string

# write csv_string to csv file
def write_string_to_csv(input_string):

    print("Writing to clan_battles_results.csv...")

    with open("clan_battles_results.csv", "w") as output:
        output.write(input_string)

######################### main ##########################################
print("Script starting...")

battle_list = load_battle_data(get_json_files())
battle_list = sorted(battle_list, key = lambda b: b['finished_at'] )

for battle in battle_list:
    CSV_STRING = translate_battle_data(battle, CSV_STRING)

write_string_to_csv(CSV_STRING)

print("Finished.")