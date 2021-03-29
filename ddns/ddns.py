#!/usr/bin/python3

import requests, datetime, yaml
from colorama import Fore, Style
from time import sleep

# CloudFlare api url.
CLOUDFLARE_URL = 'https://api.cloudflare.com/client/v4'

# Open config file
config = yaml.safe_load(open("config.yaml"))

TTL = str(config["TTL"])
if TTL == "" or TTL is None:
    print(Fore.YELLOW + "[WARN] " + Style.RESET_ALL + "TTL is empty in the config file! Using 120 instead.")
    TTL = "120"
else:
    # Try/except to see if TTL can be converted to int
    try:
        int(TTL)
        if int(TTL) < 120:
            print(Fore.YELLOW + "[WARN] " + Style.RESET_ALL + "TTL can't be below 120! Using 120 instead.")
            TTL = "120"
    except ValueError:
        print(Fore.YELLOW + "[WARN] " + Style.RESET_ALL + "TTL has been set incorrectly! Using 120 instead.")
        TTL = "120"

RECORD_TYPE = config["Record-Type"].upper()
if RECORD_TYPE != "A" and RECORD_TYPE != "AAAA":
    print(Fore.RED + "[ERROR] " + Style.RESET_ALL + "Record Type has been set incorrectly! Choose A or AAAA")
    exit()

EMAIL = config["CloudFlare-email"]
if EMAIL is None or EMAIL == "":
    print(Fore.RED + "[ERROR] " + Style.RESET_ALL + "No email was found in the config file.")
    exit()

API_KEY = config["Global-API-Key"]
if API_KEY is None or API_KEY == "":
    print(Fore.RED + "[ERROR] " + Style.RESET_ALL + "No API key was found in the config file.")
    exit()

DOMAIN = config["Domain"]
if DOMAIN is None or DOMAIN == "":
    print(Fore.RED + "[ERROR] " + Style.RESET_ALL + "No domain was found in the config file.")
    exit()

USING_ROOT = config["using-root-domain"]
if not (USING_ROOT is True or USING_ROOT is False):
    print(Fore.RED + "[ERROR] " + Style.RESET_ALL + "Using-root-domain is not set in the config file.")
    exit()

SUBDOMAIN = config["Subdomain"]
if USING_ROOT is False:
    if SUBDOMAIN is None or SUBDOMAIN == "":
        print(Fore.RED + "[ERROR] " + Style.RESET_ALL + "No subdomain was found in the config file.")
        exit()

auth_headers = {'X-Auth-Key': API_KEY, 'X-Auth-Email': EMAIL}

cached_ip = ""

def get_zone_id():
    r = requests.get(CLOUDFLARE_URL + '/zones', headers = auth_headers).json()
    if r["success"]:
        result = r["result"]
        for domain in result:
            if domain["name"] == DOMAIN:
                return domain["id"]
            else:
                continue
        # If function doesn't return, domain is invalid
        print(Fore.RED + "[ERROR] " + Style.RESET_ALL + f"No domain named \"{DOMAIN}\" was found on your cloudflare account, or check if you spelled it wrong.")
        exit()

    # Check for errors if api response wasn't a success.
    else:
        if r["errors"][0]["error_chain"][0]["code"] == 6103:
            print(Fore.RED + "[ERROR] " + Style.RESET_ALL + "You have inputted an invalid CloudFlare API token!")
            exit()
        elif r["errors"][0]["error_chain"][0]["code"] == 6102:
            print(Fore.RED + "[ERROR] " + Style.RESET_ALL + "You have inputted an invalid CloudFlare Email!")
            exit()

def get_record(domain):
    ZONE_ID = get_zone_id()
    r = requests.get(CLOUDFLARE_URL + '/zones/' + ZONE_ID + '/dns_records', headers = auth_headers).json()
    for dns_record in r["result"]:
        if dns_record["name"] == domain:
            return dns_record
        else:
            continue
    # If function doesn't return, a dns record wasn't found.
    print(Fore.RED + "[ERROR] " + Style.RESET_ALL + f"No record called \"{domain}\" was found in your cloudflare dns list, create one, or check if you spelled it wrong.")
    exit()

def get_public_ip():
    # List of IP API's just in case one is down
    # All these api urls return text
    ip_apis = ["https://ipv4.icanhazip.com/", "https://api.ipify.org/", "https://ip.seeip.org/"]
    for api_url in ip_apis:
        r = requests.get(api_url)
        if r.status_code == 200:
            ip = r.text.strip()
            return ip
        else:
            continue
    # Nothing returned, AKA all api's are down, or internet problems.
    print(Fore.YELLOW + "[WARN] " + Style.RESET_ALL + "Could not reach any ip api. Skipping this cycle.")
    return None

def update_dns_record():
    # Get public IP (current ip)
    current_ip = get_public_ip()
    if current_ip is None:
        return

    if USING_ROOT:
        domain = DOMAIN
    else:
        domain = SUBDOMAIN + "." + DOMAIN

    dns_data = get_record(domain)

    if current_ip != dns_data["content"]:
        zone_id = get_zone_id()
        dns_data['content'] = current_ip
        requests.put(CLOUDFLARE_URL+ '/zones/'+ zone_id + '/dns_records/' + dns_data['id'], headers=auth_headers, json=dns_data).json()

if "__main__" == __name__:
    while True:
        try:
            update_dns_record()
            print("DDNS Update successful!")
            print("Datetime: {}".format(datetime.datetime.now().strftime("%Y-%m-%d, %H:%M")))
        except Exception:
            print("DDNS Update failed.")
            print("Datetime: {}".format(datetime.datetime.now().strftime("%Y-%m-%d, %H:%M")))
        print("------------------------")
        print()
        sleep(900)