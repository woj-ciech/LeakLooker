from hurry.filesize import size
from colorama import Fore
import json
import shodan
import sys
import argparse
import signal

def signal_handler(signal, frame):
    print("\nSearch Finished\n")
    sys.exit(0)

description = r"""
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
LeakLooker - Find open databases
https://medium.com/@woj_ciech https://github.com/woj-ciech/
Example: python leaklooker.py --mongodb --couchdb --kibana --elastic --first 21 --last 37"""

print (description)

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter #added to show default value
)

group = parser.add_argument_group("Pages")

parser.add_argument("--elastic", help="Elasti search", action='store_true')
parser.add_argument("--couchdb", help="CouchDB" ,action='store_true')
parser.add_argument("--mongodb", help="MongoDB", action='store_true')
parser.add_argument('--kibana', help='Kibana', action='store_true')
group.add_argument('--first', help='First page', default=None, type=int)
group.add_argument('--last', help='Last page', default=None, type=int)

args = parser.parse_args()

elastic = args.elastic
couchdb = args.couchdb
mongodb = args.mongodb
kibana = args.kibana
first = args.first
last = args.last

if first and last is None:
    print ("Correct pages")
    sys.exit()
elif last and first is None:
    print ('Correct pages')
    sys.exit()
elif first is None and last is None:
    print ("Choose pages to search")
    sys.exit()
elif first > last:
    print ('Correct pages')
    sys.exit()
else:
    last = last+1

SHODAN_API_KEY = ''

query_elastic = 'product:elastic port:9200 '
query_mongodb = 'product:MongoDB '
query_couchdb = "product:couchdb "
query_kibana = "kibana content-length: 217 "

signal.signal(signal.SIGINT, signal_handler)
def shodan_query(query, page):
    try:
        api = shodan.Shodan(SHODAN_API_KEY)
        result = api.search(query, page=page)
    except shodan.APIError as e:
        print (Fore.RED + e.value + Fore.RESET)
        return False

    if len(result['matches']) > 0:
        print ('Found ' + str(result['total']) + " results")

    else:
        print ("Nothing was found")
        return False

    return result

def check_elastic(results):
    if results:
        for service in results['matches']:
            try:
                if service['elastic']['cluster']['indices']['store']['size_in_bytes'] > 217000000:
                    print ("IP: http://" + Fore.LIGHTGREEN_EX  + service['ip_str'] + ':' + str(service['port']) + '/_cat/indices?v' + Fore.RESET)
                    print ("Size: "+ Fore.LIGHTGREEN_EX  + size(service['elastic']['cluster']['indices']['store']['size_in_bytes']) + Fore.RESET)
                    try:
                        print('Country: ' + Fore.LIGHTBLUE_EX + service['location']['country_name'] + Fore.RESET)
                    except:
                        print ('Country: ' + Fore.RED + 'Unknown' + Fore.RESET)
                    print ("Indices: ")
                    for indice,info in service['elastic']['indices'].items():
                        print (Fore.GREEN + indice + Fore.RESET)
                    print ("-----------------------------")
            except KeyError:
                pass

def check_mongodb(results):
    if results:
        for service in results['matches']:

            try:
                if service['mongodb']['listDatabases']['totalSize'] > 217000000:
                    print ("IP: " + Fore.LIGHTBLUE_EX + service['ip_str'] + Fore.RESET)
                    print ("Size: " + Fore.LIGHTBLUE_EX + size(service['mongodb']['listDatabases']['totalSize']) + Fore.RESET)
                    try:
                        print('Country: ' + Fore.LIGHTBLUE_EX + service['location']['country_name'] + Fore.RESET)
                    except:
                        print ('Country: ' + Fore.RED + 'Unknown' + Fore.RESET)
                    for database in service['mongodb']['listDatabases']['databases']:
                        if database['empty'] != 'true':
                            print ("Database name: " + Fore.BLUE + database['name'] + Fore.RESET)
                            print("Size: " + Fore.BLUE + size(database['sizeOnDisk']) + Fore.RESET)
                            print ('Collections: ')
                            for collection in database['collections']:
                                print (Fore.LIGHTBLUE_EX + collection + Fore.RESET)
                    print ("-----------------------------")
            except KeyError:
                pass

def check_couchdb(results):
    if results:
        for service in results['matches']:
            try:
                data = service['data']
                if "200 OK" in data:
                    response = data.splitlines()
                    for line in response:
                        if line.startswith("{"):
                            json_data = json.loads(line)
                            if len(json_data['dbs']) < 20 and 'compromised' not in service['tags']:
                                print ("IP: http://" + Fore.YELLOW + service['ip_str'] + ':' + str(service['port']) + '/_utils' + Fore.RESET)
                                try:
                                    print('Country: ' + Fore.LIGHTBLUE_EX + service['location'][
                                        'country_name'] + Fore.RESET)
                                except:
                                    print('Country: ' + Fore.RED + 'Unknown' + Fore.RESET)
                                for db in json_data['dbs']:
                                    print (Fore.LIGHTYELLOW_EX + db + Fore.RESET)

                            print ("-----------------------------")
            except KeyError:
                pass

def check_kibana(results):
    if results:
        try:
            for service in results['matches']:
                if "200 OK" in service['data']:
                    print("IP: http://" + Fore.CYAN + service['ip_str'] + ':' + str(
                        service['port']) + '/app/kibana#/discover?_g=()' + Fore.RESET)
                    try:
                        print('Country: ' + Fore.LIGHTBLUE_EX + service['location']['country_name'] + Fore.RESET)
                    except:
                        print ('Country: ' + Fore.RED + 'Unknown' + Fore.RESET)
                        print ('---')
                    print ('---')
        except:
            pass


if elastic:
    for page in range (first,last):
        print (Fore.RED + '----------------------------------Elastic - Page ' + str(page) + '--------------------------------' + Fore.RESET)
        elastic_results = shodan_query(query_elastic, page)
        check_elastic(elastic_results)

if couchdb:
    for page in range (first,last):
        print (Fore.RED + '----------------------------------CouchDB - Page ' + str(page) + '--------------------------------' + Fore.RESET)
        couchdb_results = shodan_query(query_couchdb, page)
        check_couchdb(couchdb_results)

if mongodb:
    for page in range (first,last):
        print (Fore.RED + '----------------------------------MongoDB - Page ' + str(page) + '--------------------------------' + Fore.RESET)
        mongodb_results = shodan_query(query_mongodb, page)
        check_mongodb(mongodb_results)

if kibana:
    for page in range (first,last):
        print (Fore.RED + '----------------------------------Kibana - Page ' + str(page) + '--------------------------------' + Fore.RESET)
        kibana_results = shodan_query(query_kibana, page)
        check_kibana(kibana_results)
