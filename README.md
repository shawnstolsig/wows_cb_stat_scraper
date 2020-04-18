# wows_cb_stat_scraper
A World of Warships Clan Battles stats script.  Transforms JSON files downloaded from WG to CSV file that can be easily copy/pasted into other KSC/KSD/KSE clan spreadsheets.

Note that the main file of interest here is cb_stats.py.  



### Dependencies:
Python 3.8

Built in packages: datetime, json, os

External packages: pytz

##### Running/Building:
You can run from terminal using command (ensure same-season json files are in the same folder before running): 

python cb_stats.py 


Optionally, you can build to a single-file executable using pyinstaller.  After installing pyinstaller, you can build a .exe with the following command: 

pyinstaller cb_stats.py -F --icon=logo.ico


