# wows_cb_stat_scraper
A World of Warships Clan Battles stats script.  Transforms JSON files downloaded from WG to CSV file that can be easily copy/pasted into other KSC/KSD/KSE clan spreadsheets.

Note that the main file of interest here is cb_stats.py.  



### Dependencies:
Python 3.8

Built in packages: datetime, json, os

External packages: pytz

### Running/Building:
Place same-season json files from WG into the same folder as the script.  Run with command: 

python cb_stats.py 


Optionally, you can build to a single-file executable using pyinstaller.  After installing pyinstaller, you can build a .exe with the following command: 

pyinstaller cb_stats.py -F --icon=logo.ico

### Other
JSON files can be optained from links below.  Note that you must be first be authenticated through the World of Warships website for these links to work.  Also, they will only return the 50 most recent battles played, per rating. 

Alpha: https://clans.worldofwarships.com/clans/wows/ladder/api/battles/?team=1

Bravo: https://clans.worldofwarships.com/clans/wows/ladder/api/battles/?team=2

