import os
import json
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from googlesearch import search
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

API_FILE = ".api_keys.json"

def banner():
    ascii_art = f"""{Fore.CYAN}
  ____  _           _                           
 / ___|| |__   __ _| | ___  _ __ ___   ___ _ __ 
 \___ \| '_ \ / _` | |/ _ \| '_ ` _ \ / _ \ '__|
  ___) | | | | (_| | | (_) | | | | | |  __/ |   
 |____/|_| |_|\__,_|_|\___/|_| |_| |_|\___|_|   
{Fore.YELLOW}         Peace shouldn't be an option
{Fore.MAGENTA}                 Script by Shadow
{Style.RESET_ALL}"""
    print(ascii_art)

def save_api_keys(keys):
    with open(API_FILE, "w") as f:
        json.dump(keys, f, indent=4)

def load_or_set_api_keys():
    if os.path.exists(API_FILE):
        with open(API_FILE, "r") as f:
            return json.load(f)
    else:
        print(Fore.YELLOW + "[!] First-Time Setup: API Keys")
        keys = {}
        keys["numverify_key"] = input("Enter NumVerify API Key (or leave blank to skip): ").strip()
        keys["twilio_sid"] = input("Enter Twilio SID (or leave blank to skip): ").strip()
        keys["twilio_auth"] = input("Enter Twilio Auth Token (or leave blank to skip): ").strip()
        save_api_keys(keys)
        print(Fore.GREEN + "[✓] API keys saved in .api_keys.json. Edit this file manually to update/delete.")
        return keys

def basic_info(number):
    try:
        parsed = phonenumbers.parse(number, None)
        return {
            "Valid Number": phonenumbers.is_valid_number(parsed),
            "Possible Number": phonenumbers.is_possible_number(parsed),
            "Country": geocoder.description_for_number(parsed, "en"),
            "Carrier": carrier.name_for_number(parsed, "en"),
            "Timezones": timezone.time_zones_for_number(parsed)
        }
    except:
        return {"Error": "Invalid number format."}

def numverify_api(number, api_key):
    if not api_key:
        return {"Note": "NumVerify API Key not provided."}
    try:
        url = f"http://apilayer.net/api/validate?access_key={api_key}&number={number}&country_code=&format=1"
        res = requests.get(url).json()
        return res
    except:
        return {"Error": "Failed to fetch from NumVerify API."}

def twilio_lookup(number, sid, auth):
    if not sid or not auth:
        return {"Note": "Twilio credentials not provided."}
    try:
        url = f"https://lookups.twilio.com/v1/PhoneNumbers/{number}?Type=carrier"
        res = requests.get(url, auth=(sid, auth)).json()
        return res
    except:
        return {"Error": "Twilio lookup failed."}

def google_dump(number):
    try:
        links = list(search(number, num_results=10))
        return links
    except:
        return ["Error: Google search failed or blocked."]

def truecaller_lookup(number):
    return {"Truecaller": "Manual scraping or mobile automation required."}

def check_apps(number):
    return {
        "WhatsApp": "Check via WhatsApp contact sync",
        "Telegram": "Check via Telegram import or sync"
    }

def save_result(data):
    with open("number_info_dump.json", "w") as f:
        json.dump(data, f, indent=4)
    print(Fore.GREEN + "\n[✓] Data saved in 'number_info_dump.json'.")

def print_section(title, data):
    print(f"\n{Fore.BLUE + '='*50}")
    print(Fore.CYAN + f"{title}")
    print(Fore.BLUE + '='*50)
    for k, v in data.items():
        print(Fore.YELLOW + f"{k}: {Fore.WHITE}{v}")

def main():
    os.system("clear" if os.name != "nt" else "cls")
    banner()

    number = input(Fore.CYAN + "[?] Enter phone number with country code (e.g., +919999999999): ").strip()
    api_keys = load_or_set_api_keys()

    result = {}

    basic = basic_info(number)
    print_section("Basic Number Info", basic)
    result["Basic_Info"] = basic

    numverify = numverify_api(number, api_keys.get("numverify_key"))
    print_section("NumVerify API Result", numverify)
    result["NumVerify"] = numverify

    twilio = twilio_lookup(number, api_keys.get("twilio_sid"), api_keys.get("twilio_auth"))
    print_section("Twilio Lookup Result", twilio)
    result["Twilio"] = twilio

    truecaller = truecaller_lookup(number)
    print_section("Truecaller Info", truecaller)
    result["Truecaller"] = truecaller

    apps = check_apps(number)
    print_section("App Presence", apps)
    result["App_Presence"] = apps

    g_links = google_dump(number)
    print(Fore.MAGENTA + "\nGoogle Search Results:")
    for link in g_links:
        print(Fore.CYAN + f"- {link}")
    result["Google_Results"] = g_links

    save_result(result)

if __name__ == "__main__":
    main()
