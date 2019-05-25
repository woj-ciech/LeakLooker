from hurry.filesize import size
from colorama import Fore
import json
import shodan
import sys
import argparse
from bs4 import BeautifulSoup

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

print(description)

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter  # added to show default value
)

group = parser.add_argument_group("Pages")

parser.add_argument("--elastic", help="Elasti search", action='store_true')
parser.add_argument("--couchdb", help="CouchDB", action='store_true')
parser.add_argument("--mongodb", help="MongoDB", action='store_true')

parser.add_argument("--samba", help="Samba", action='store_true')
parser.add_argument("--gitlab", help="Gitlab", action='store_true')
parser.add_argument("--rsync", help="Rsync", action='store_true')
parser.add_argument("--jenkins", help="Jenkins", action='store_true')
parser.add_argument("--sonarqube", help="SonarQube", action='store_true')
parser.add_argument("--query", help="Additional query or filter for Shodan", default="")


parser.add_argument('--kibana', help='Kibana', action='store_true')
group.add_argument('--first', help='First page', default=None, type=int)
group.add_argument('--last', help='Last page', default=None, type=int)

args = parser.parse_args()

samba = args.samba
gitlab = args.gitlab
rsync = args.rsync
jenkins = args.jenkins
sonarqube = args.sonarqube
query = args.query

elastic = args.elastic
couchdb = args.couchdb
mongodb = args.mongodb
kibana = args.kibana
first = args.first
last = args.last

if first and last is None:
    print("Correct pages")
    sys.exit()
elif last and first is None:
    print('Correct pages')
    sys.exit()
elif first is None and last is None:
    print("Choose pages to search")
    sys.exit()
elif first > last:
    print('Correct pages')
    sys.exit()
else:
    last = last + 1

SHODAN_API_KEY = ''

query_elastic = 'product:elastic port:9200 '
query_mongodb = 'product:MongoDB '
query_couchdb = "product:couchdb "
query_kibana = "kibana content-length: 217 "
query_gitlab = "http.favicon.hash:1278323681"
query_rsync = "product:rsyncd"
query_sonarqube = "sonarqube"
query_jenkins = "jenkins 200 ok"
query_samba = "product:samba disabled"


def shodan_query(query, page):
    try:
        api = shodan.Shodan(SHODAN_API_KEY)
        result = api.search(query, page=page)
    except shodan.APIError as e:
        print(Fore.RED + e.value + Fore.RESET)
        return False

    if len(result['matches']) > 0:
        print('Found ' + str(result['total']) + " results")

    else:
        print("Nothing was found")
        return False

    return result


def check_samba(results):
    if results:
        try:
            for service in results['matches']:
                if service['smb']['anonymous'] == True:
                    print(Fore.LIGHTGREEN_EX + service['ip_str'] + ':' + str(service['port']) + Fore.RESET)
                    if service['hostnames']:
                        print("Hostname")
                        for hostname in service['hostnames']:
                            print(Fore.LIGHTYELLOW_EX + hostname + Fore.RESET)
                    try:
                        print('Country: ' + Fore.LIGHTBLUE_EX + service['location']['country_name'] + Fore.RESET)
                    except:
                        print('Country: ' + Fore.RED + 'Unknown' + Fore.RESET)

                    print("Shares")
                    for share in service['smb']['shares']:
                        print(Fore.CYAN + share['name'] + " - " + share['comments'] + Fore.RESET)
                    print("-----------------------------")
        except Exception as e:
            pass


def check_elastic(results):
    if results:
        for service in results['matches']:
            try:
                if service['elastic']['cluster']['indices']['store']['size_in_bytes'] > 217000000:
                    print("IP: http://" + Fore.LIGHTGREEN_EX + service['ip_str'] + ':' + str(
                        service['port']) + '/_cat/indices?v' + Fore.RESET)
                    if service['hostnames']:
                        print("Hostname")
                        for hostname in service['hostnames']:
                            print(Fore.LIGHTYELLOW_EX + hostname + Fore.RESET)
                    print("Size: " + Fore.LIGHTGREEN_EX + size(
                        service['elastic']['cluster']['indices']['store']['size_in_bytes']) + Fore.RESET)
                    try:
                        print('Country: ' + Fore.LIGHTBLUE_EX + service['location']['country_name'] + Fore.RESET)
                    except:
                        print('Country: ' + Fore.RED + 'Unknown' + Fore.RESET)
                    print("Indices: ")
                    for indice, info in service['elastic']['indices'].items():
                        print(Fore.GREEN + indice + Fore.RESET)
                    print("-----------------------------")
            except KeyError:
                pass


def check_mongodb(results):
    if results:
        for service in results['matches']:

            try:
                if service['mongodb']['listDatabases']['totalSize'] > 217000000:
                    print("IP: " + Fore.LIGHTBLUE_EX + service['ip_str'] + Fore.RESET)
                    if service['hostnames']:
                        print("Hostname")
                        for hostname in service['hostnames']:
                            print(Fore.LIGHTYELLOW_EX + hostname + Fore.RESET)
                    print("Size: " + Fore.LIGHTBLUE_EX + size(
                        service['mongodb']['listDatabases']['totalSize']) + Fore.RESET)
                    try:
                        print('Country: ' + Fore.LIGHTBLUE_EX + service['location']['country_name'] + Fore.RESET)
                    except:
                        print('Country: ' + Fore.RED + 'Unknown' + Fore.RESET)
                    for database in service['mongodb']['listDatabases']['databases']:
                        if database['empty'] != 'true':
                            print("Database name: " + Fore.BLUE + database['name'] + Fore.RESET)
                            print("Size: " + Fore.BLUE + size(database['sizeOnDisk']) + Fore.RESET)
                            print('Collections: ')
                            for collection in database['collections']:
                                print(Fore.LIGHTBLUE_EX + collection + Fore.RESET)
                    print("-----------------------------")
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
                                print("IP: http://" + Fore.YELLOW + service['ip_str'] + ':' + str(
                                    service['port']) + '/_utils' + Fore.RESET)
                                if service['hostnames']:
                                    print("Hostname")
                                    for hostname in service['hostnames']:
                                        print(Fore.LIGHTYELLOW_EX + hostname + Fore.RESET)
                                try:
                                    print('Country: ' + Fore.LIGHTBLUE_EX + service['location'][
                                        'country_name'] + Fore.RESET)
                                except:
                                    print('Country: ' + Fore.RED + 'Unknown' + Fore.RESET)
                                print("Databases")
                                for db in json_data['dbs']:
                                    print(Fore.LIGHTYELLOW_EX + db + Fore.RESET)

                            print("-----------------------------")
            except KeyError:
                pass


def check_kibana(results):
    if results:
        try:
            for service in results['matches']:
                if "200 OK" in service['data']:
                    print("IP: http://" + Fore.CYAN + service['ip_str'] + ':' + str(
                        service['port']) + '/app/kibana#/discover?_g=()' + Fore.RESET)
                    if service['hostnames']:
                        print("Hostname")
                        for hostname in service['hostnames']:
                            print(Fore.LIGHTYELLOW_EX + hostname + Fore.RESET)
                    try:
                        print('Country: ' + Fore.LIGHTBLUE_EX + service['location']['country_name'] + Fore.RESET)
                    except:
                        print('Country: ' + Fore.RED + 'Unknown' + Fore.RESET)
                        print('---')
                    print('---')
        except:
            pass


def check_jenkins(results):
    if results:
        for service in results['matches']:
            executors = set()
            jobs = set()
            if 'http' in service:
                print(Fore.LIGHTGREEN_EX + "http://" + service['ip_str'] + ':' + str(service['port']) + Fore.RESET)
                if service['hostnames']:
                    print("Hostname")
                    for hostname in service['hostnames']:
                        print(Fore.LIGHTYELLOW_EX + hostname + Fore.RESET)
                try:
                    print('Country: ' + Fore.LIGHTBLUE_EX + service['location']['country_name'] + Fore.RESET)
                except:
                    print('Country: ' + Fore.RED + 'Unknown' + Fore.RESET)
                soup = BeautifulSoup(service['http']['html'], features="html.parser")
                for project in soup.find_all("a", {"class": "model-link inside"}):
                    if project['href'].startswith("/computer"):
                        splitted = project['href'].split("/")
                        executors.add(splitted[2])

                    elif project['href'].startswith("job"):
                        splitted = project['href'].split("/")
                        jobs.add(splitted[1])

                print(Fore.BLUE + "Executors" + Fore.RESET)
                for executor in executors:
                    print(Fore.CYAN + executor + Fore.RESET)

                print(Fore.BLUE + "Jobs" + Fore.RESET)
                for job in jobs:
                    print(Fore.CYAN + job + Fore.RESET)
            print("-----------------------------")


def check_sonarqube(results):
    if results:
        for service in results['matches']:
            print(Fore.LIGHTGREEN_EX + "https://" + service['ip_str'] + ':' + str(service['port']) + Fore.RESET)
            if service['hostnames']:
                print("Hostname")
                for hostname in service['hostnames']:
                    print(Fore.LIGHTYELLOW_EX + hostname + Fore.RESET)
            try:
                print('Country: ' + Fore.LIGHTBLUE_EX + service['location']['country_name'] + Fore.RESET)
            except:
                print('Country: ' + Fore.RED + 'Unknown' + Fore.RESET)
            print("-----------------------------")

def check_gitlab(results):
    if results:
        for service in results['matches']:
            if 'http' in service:
                if "register" in service['http']['html']:
                    print(Fore.LIGHTGREEN_EX + "https://" + service['ip_str'] + ':' + str(service['port']) + Fore.RESET)
                    if service['hostnames']:
                        print("Hostname")
                        for hostname in service['hostnames']:
                            print(Fore.LIGHTYELLOW_EX + hostname + Fore.RESET)
                    try:
                        print('Country: ' + Fore.LIGHTBLUE_EX + service['location']['country_name'] + Fore.RESET)
                    except:
                        print('Country: ' + Fore.RED + 'Unknown' + Fore.RESET)
                    print("-----------------------------")

def check_rsync(results):
    if results:
        for service in results['matches']:
            if service['rsync']['authentication'] == False and service['rsync']['modules']:
                print(Fore.LIGHTGREEN_EX + "rsync://" + service['ip_str'] + ':' + str(service['port']) + Fore.RESET)
                if service['hostnames']:
                    print("Hostname")
                    for hostname in service['hostnames']:
                        print(Fore.LIGHTYELLOW_EX + hostname + Fore.RESET)
                try:
                    print('Country: ' + Fore.LIGHTBLUE_EX + service['location']['country_name'] + Fore.RESET)
                except:
                    print('Country: ' + Fore.RED + 'Unknown' + Fore.RESET)

                modules = [*service['rsync']['modules']]
                print ("Modules")
                for module in modules:
                    print(Fore.LIGHTMAGENTA_EX + module + Fore.RESET)
                print("-----------------------------")

if rsync:
    for page in range(first,last):
        print(Fore.RED + '----------------------------------Rsync - Page ' + str(
            page) + '--------------------------------' + Fore.RESET)
        rsync_results = shodan_query(query_rsync + " " + query,page)
        check_rsync(rsync_results)

if gitlab:
    for page in range(first,last):
        print(Fore.RED + '----------------------------------GitLab - Page ' + str(
            page) + '--------------------------------' + Fore.RESET)
        gitlab_results = shodan_query(query_gitlab+ " " + query,page)
        check_gitlab(gitlab_results)

if sonarqube:
    for page in range(first, last):
        print(Fore.RED + '----------------------------------SonarQube - Page ' + str(
            page) + '--------------------------------' + Fore.RESET)
        sonarqube_results = shodan_query(query_sonarqube+ " " + query, page)
        check_sonarqube(sonarqube_results)

if jenkins:
    for page in range(first, last):
        print(Fore.RED + '----------------------------------Jenkins - Page ' + str(
            page) + '--------------------------------' + Fore.RESET)
        jenkins_results = shodan_query(query_jenkins+ " " + query, page)
        check_jenkins(jenkins_results)

if samba:
    for page in range(first, last):
        print(Fore.RED + '----------------------------------Samba - Page ' + str(
            page) + '--------------------------------' + Fore.RESET)
        samba_results = shodan_query(query_samba+ " " + query, page)
        check_samba(samba_results)

if elastic:
    for page in range(first, last):
        print(Fore.RED + '----------------------------------Elastic - Page ' + str(
            page) + '--------------------------------' + Fore.RESET)
        elastic_results = shodan_query(query_elastic+ " " + query, page)
        check_elastic(elastic_results)

if couchdb:
    for page in range(first, last):
        print(Fore.RED + '----------------------------------CouchDB - Page ' + str(
            page) + '--------------------------------' + Fore.RESET)
        couchdb_results = shodan_query(query_couchdb+ " " + query, page)
        check_couchdb(couchdb_results)

if mongodb:
    for page in range(first, last):
        print(Fore.RED + '----------------------------------MongoDB - Page ' + str(
            page) + '--------------------------------' + Fore.RESET)
        mongodb_results = shodan_query(query_mongodb+ " " + query, page)
        check_mongodb(mongodb_results)

if kibana:
    for page in range(first, last):
        print(Fore.RED + '----------------------------------Kibana - Page ' + str(
            page) + '--------------------------------' + Fore.RESET)
        kibana_results = shodan_query(query_kibana+ " " + query, page)
        check_kibana(kibana_results)