import json
import os
from datetime import datetime, timedelta

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

# update both SHIP_INDEX_TABLE and csv_string headers whenever new ships added
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
CSV_STRING = "Date,Session,Clan,Rating,Opponent,#,Map,Notes,Ya,Sk,Mo,Oh,Kr,GK,Co,Th,Re,Bo,Za,DM,Sa,Hi,Go,He,Ve,Yo,PR,Pp,Mk,St,Wo,Nv,Sm,Mi,Co,Sh,Hg,Hy,Ge,So,Gr,Kh,52,Da,Kl,Ma,PE,Hd,Sd,YY,Hk,Md,FR,MR,Au,X,,0,Points\n"

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
    
    data_time_obj_new_local = datetime.fromtimestamp(float(date_time_iso)

    print(f'date_time_iso: {date_time_iso}')
    print(f'data_time_obj_new_local: {data_time_obj_new_local}')
    print(f'date_time_obj_utc: {date_time_obj_utc}')
    print(f'date_time_obj_local: {date_time_obj_local}')
    print(f'date_time: {date_time}')

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
    csv_string += f"{date_time},{SESSION_IDS[date_time]},{own_clan_tag},{own_clan_rating},{opponent_tag},script,{map_name},,{sl[0]},{sl[1]},{sl[2]},{sl[3]},{sl[4]},{sl[5]},{sl[6]},{sl[7]},{sl[8]},{sl[9]},{sl[10]},{sl[11]},{sl[12]},{sl[13]},{sl[14]},{sl[15]},{sl[16]},{sl[17]},{sl[18]},{sl[19]},{sl[20]},{sl[21]},{sl[22]},{sl[23]},{sl[24]},{sl[25]},{sl[26]},{sl[27]},{sl[28]},{sl[29]},{sl[30]},{sl[31]},{sl[32]},{sl[33]},{sl[34]},{sl[35]},{sl[36]},,,{result},{rating_delta}\n"

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