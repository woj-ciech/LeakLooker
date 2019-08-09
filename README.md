# LeakLooker - Powered by Binaryedge.io
Find open databases/services

New version supports:
- Elasticsearch
- CouchDB
- MongoDB
- Gitlab
- Rsync
- Jenkins
- Sonarqube
- Kibana
- CassandraDB
- RethinkDB
- Directory listing

and custom query.

Queries:

https://docs.binaryedge.io/api-v2/

Background:

v1: https://medium.com/@woj_ciech/leaklooker-find-open-databases-in-a-second-9da4249c8472

v2: https://medium.com/hackernoon/leaklooker-v2-find-more-open-servers-and-source-code-leaks-25e671700e41

v3: https://medium.com/@woj_ciech/leaklooker-part-3-dna-samples-internal-files-and-more-967e794fa031

## Requirements:
Python 3 &
Binaryedge API

***Paste your BinaryEdge API key in line 113***
```
pip3 install colorama
pip3 install hurry.filesize
pip3 install beautifulsoup4
```

```
pip install -r requirements.txt
```

## Usage
```
(venv) root@kali:~/PycharmProjects/LeakLooker# python leaklooker.py -h

         ,
         )\
        /  \
       '  # '
       ',  ,'
         `'

         ,
         )\
        /  \
       '  ~ '
       ',  ,'
         `'
LeakLooker - Find open databases - Powered by Binaryedge.io
https://medium.com/@woj_ciech https://github.com/woj-ciech/
Example: python leaklooker.py --mongodb --couchdb --kibana --elastic --first 21 --last 37
usage: leaklooker.py [-h] [--elastic] [--couchdb] [--mongodb] [--gitlab]
                     [--rsync] [--jenkins] [--sonarqube] [--query QUERY]
                     [--cassandra] [--rethink] [--listing] [--kibana]
                     [--first FIRST] [--last LAST]

optional arguments:
  -h, --help     show this help message and exit
  --elastic      Elastic search (default: False)
  --couchdb      CouchDB (default: False)
  --mongodb      MongoDB (default: False)
  --gitlab       Gitlab (default: False)
  --rsync        Rsync (default: False)
  --jenkins      Jenkins (default: False)
  --sonarqube    SonarQube (default: False)
  --query QUERY  Additional query or filter for BinaryEdge (default: )
  --cassandra    Cassandra DB (default: False)
  --rethink      Rethink DB (default: False)
  --listing      Listing directory (default: False)
  --kibana       Kibana (default: False)

Pages:
  --first FIRST  First page (default: None)
  --last LAST    Last page (default: None)

```

***You need to specify first and last page***

## Example

### Search for RethinkDB and listing directory in pages from 21 to 37
```
root@kali:~/PycharmProjects/LeakLooker# python leaklooker.py --rethink --listing --first 21 --last 37
----------------------------------Listing directory - Page 21--------------------------------
https://[REDACTED]:6666
Product: Apache httpd
Hostname: localhost
[REDACTED]/
[REDACTED]/
[REDACTED]/
[REDACTED]/
[REDACTED]/
-----------------------------
https://[REDACTED]:6666
Product: MiniServ
-----------------------------
https://[REDACTED]:6666
Product: Apache httpd
[REDACTED]/
[REDACTED]/
[REDACTED].html
[REDACTED]/
[REDACTED].css
[REDACTED]/
[REDACTED]/
[REDACTED]/
favicon.ico
-----------------------------
https://[REDACTED]:6666
Product: Apache httpd
[REDACTED]/
[REDACTED]/
[REDACTED]/
[REDACTED]..>
[REDACTED]/
[REDACTED]..>
[REDACTED]/
----------------------------------Rethink DB - Page 21--------------------------------
ReQL: [REDACTED]:28015
HTTP Admin: http://[REDACTED]:8080
Hostname: [REDACTED]
Version: rethinkdb 2.3.6~0trusty (GCC 4.8.2)
Name: [REDACTED]
Database: [REDACTED]
Tables: 
Database: rethinkdb
Tables: 
cluster_config
current_issues
db_config
jobs
logs
permissions
server_config
server_status
stats
table_config
table_status
users
Database: [REDACTED]
Tables: 
-----------------------------
ReQL: [REDACTED]:28015
HTTP Admin: http://[REDACTED]:8080
Hostname: [REDACTED]
Version: rethinkdb 2.3.6~0jessie (GCC 4.9.2)
Name: [REDACTED]
Database: [REDACTED]
Tables: 
Database: rethinkdb
Tables: 
cluster_config
current_issues
db_config
jobs
logs
permissions
server_config
server_status
stats
table_config
table_status
users
Database: settings
Tables: 
-----------------------------

```

### Search for Jenkins, Gitlab in Uruguay (Country code is UY) on pages from 1 to 2
```
root@kali:~/PycharmProjects/LeakLooker# python leaklooker.py --jenkins --gitlab --first 1 --last 2 --query "country:UY"
----------------------------------GitLab - Page 1--------------------------------
Total results: 13
https://[REDACTED]:443
GitLab Community Edition
Registration is open
-----------------------
https://[REDACTED]:443
Registration is closed. Check public repositories. https://164.73.232.10:443/explore
-----------------------
https://[REDACTED]:443
Registration is closed. Check public repositories. https://190.64.138.5:443/explore
-----------------------
https://[REDACTED]:443
GitLab Community Edition
Registration is open
[...]
----------------------------------Jenkins - Page 1--------------------------------
Total results: 6501
http://[REDACTED]:443
Executors
Windows
(master)
Jobs
-----------------------------
http://[REDACTED]:443
Executors
Jobs
-----------------------------
http://[REDACTED]:443
Executors
Jobs
[REDACTED]
[REDACTED]
```
### Search for mongoDB and Elasticsearch with keyword "medical" only on first page
```
root@kali:~/PycharmProjects/LeakLooker# python leaklooker.py --mongo --elastic --first 1 --last 1 --query "medical"
```
## Additional
Tool has been made for educational purposes only. I'm not responsible for any damage caused. Don't be evil.
