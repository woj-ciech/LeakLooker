# LeakLooker
Find open databases with Shodan

Background:

https://medium.com/@woj_ciech/leaklooker-find-open-databases-in-a-second-9da4249c8472

## Requirements:
Python 3

Shodan paid plan, except Kibana search

***Put your Shodan API key in line 14***
```
python3 -m pip install -r requestments.txt
```

## Usage
```
root@kali:~/# python leaklooker.py -h

                                                            ,
                                                            )\
 _                _    _                 _                 /  \
| |              | |  | |               | |               '  # '
| |     ___  __ _| | _| |     ___   ___ | | _____ _ __    ',  ,'
| |    / _ \/ _` | |/ / |    / _ \ / _ \| |/ / _ \ '__|     `'  ,
| |___|  __/ (_| |   <| |___| (_) | (_) |   <  __/ |            )\
\_____/\___|\__,_|_|\_\_____/\___/ \___/|_|\_\___|_|           /  \
                                                              '  ~ '
                                                              ',  ,'
                                                                `'
LeakLooker - Find open databases
https://medium.com/@woj_ciech   https://github.com/woj-ciech/

usage: leaklooker.py [-h] [-e] [-c] [-m] [-k] [-f FIRST] [-l LAST] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -e, --elastic         Elasti search (default: False)
  -c, --couchdb         CouchDB (default: False)
  -m, --mongodb         MongoDB (default: False)
  -k, --kibana          Kibana (default: False)

Output:
  -o OUTPUT, --output OUTPUT
                        Output file (default: None)

Pages:
  -f FIRST, --first FIRST
                        First page (default: None)
  -l LAST, --last LAST  Last page (default: None)
```

***You need to specify first and last page***

## Example
```
root@kali:~/# python leaklooker.py --mongodb --couchdb --kibana --elastic --first 12 --last 14
[...]
----------------------------------Elastic - Page 12--------------------------------
Found 25069 results
IP: http://xxx.xxx.xxx.xxx:9200/_cat/indices?v
Size: 1G
Country: France
Indices:
.monitoring-kibana-6-2019.01.08
[...]
----------------------------
IP: http://yyy.yyy.yyy.yyy:9200/_cat/indices?v
Size: 144G
Country: China
Indices:
zhuanli
hx_person
[...]
----------------------------------CouchDB - Page 12--------------------------------
Found 5932 results
-----------------------------
IP: http://xxx.xxx.xxx:5984/_utils
Country: Austria
new_fron_db
test_db
-----------------------------
IP: http://yyy.yyy.yyy.yyy:5984/_utils
Country: United States
_replicator
_users
backup_20180917
backup_db
eio_local
tfa_pos
----------------------------------MongoDB - Page 12--------------------------------
Found 66680 results
IP: xxx.xxx.xxx.xxx
Size: 6G
Country: France
Database name: Warn
Size: 80M
Collections:
Warn
system.indexes
Database name: xhprofprod
Size: 5G
Collections:
results
system.indexes
-----------------------------
IP: yyy.yyy.yyy.yyy
Size: 544M
Country: Ukraine
Database name: local
Size: 32M
Collections:
startup_log
Database name: ace_stat
Size: 256M
Collections:
stat_minute
system.indexes
stat_hourly
stat_daily
[...]
Database name: ace
Size: 256M
Collections:
usergroup
system.indexes
scheduletask
dpigroup
portforward
wlangroup
[...]
----------------------------------Kibana - Page 12--------------------------------
Found 10464 results
IP: http://xxx.xxx.xxx.xxx:5601/app/kibana#/discover?_g=()
Country: Germany
---
IP: http://yyy.yyy.yyy.yyy:5601/app/kibana#/discover?_g=()
Country: United States
---
IP: http://zzz.zzz.zzz.zzz:5601/app/kibana#/discover?_g=()
Country: United Kingdom
```

## Screenshots
![](https://cdn-images-1.medium.com/max/800/1*Fj8DRqY9bpDmftuPK9clUA.png)

![](https://cdn-images-1.medium.com/max/600/1*-s4pZpMIU4ZbdRjuBVxRYg.png)

## Additional
Tool has been made for educational purposes only. I'm not responsible for any damage caused. Don't be evil.
