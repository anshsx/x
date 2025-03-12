import os
import json
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from googlesearch import search
from colorama import Fore, Style, init
from pyfiglet import Figlet

# Init colorama
init(autoreset=True)

API_FILE = "api.json"

def clear_terminal():
    os.system("clear" if os.name != "nt" else "cls")

def banner(text="SXPhone"):
    fig = Figlet(font='slant')  # You can change the font as desired
    ascii_art = fig.renderText(text)
    print(Fore.CYAN + ascii_art)
    print(f"""{Fore.YELLOW}Peace shouldn't be an option
{Fore.MAGENTA}Script by Shadow
""")

def setup_api_keys():
    print(f"{Fore.YELLOW}[!] First-time setup: Add API keys (optional). Leave blank to skip.")
    apis = {
        "numverify_key": "",
        "twilio_sid": "",
        "twilio_auth": "",
        "abstract_key": "",
        "numlookup_key": "",
        "apilayer_key": "",
        "anyotherapi_key": ""
    }
    for key in apis.keys():
        val = input(f"{Fore.CYAN}Enter {key} (leave blank to skip): ").strip()
        apis[key] = val if val else ""
    with open(API_FILE, "w") as f:
        json.dump(apis, f, indent=4)
    print(f"{Fore.GREEN}[✓] API keys saved in api.json (edit manually anytime).")

def load_api_keys():
    if not os.path.exists(API_FILE):
        setup_api_keys()
    with open(API_FILE, "r") as f:
        return json.load(f)

def basic_info(number):
    try:
        num = phonenumbers.parse(number)
        return {
            "Valid Number": phonenumbers.is_valid_number(num),
            "Possible Number": phonenumbers.is_possible_number(num),
            "Location": geocoder.description_for_number(num, 'en'),
            "Carrier": carrier.name_for_number(num, 'en'),
            "Timezone(s)": timezone.time_zones_for_number(num)
        }
    except:
        return {"Error": "Invalid number format."}

def numverify_lookup(number, key):
    if not key: return {}
    try:
        url = f"http://apilayer.net/api/validate?access_key={key}&number={number}"
        return requests.get(url).json()
    except: return {}

def twilio_lookup(number, sid, auth):
    if not sid or not auth: return {}
    try:
        url = f"https://lookups.twilio.com/v1/PhoneNumbers/{number}?Type=carrier"
        return requests.get(url, auth=(sid, auth)).json()
    except: return {}

def abstract_lookup(number, key):
    if not key: return {}
    try:
        url = f"https://phonevalidation.abstractapi.com/v1/?api_key={key}&phone={number}"
        return requests.get(url).json()
    except: return {}

def numlookup_io(number, key):
    if not key: return {}
    try:
        url = f"https://api.numlookupapi.com/v1/validate/{number}?apikey={key}"
        return requests.get(url).json()
    except: return {}

def google_search(number):
    try:
        links = list(search(number, num_results=10))
        return links
    except: return []

def print_section(title, data):
    if not data or all(val in ["", None, False, {}, []] for val in data.values() if isinstance(data, dict)):
        return
    print(f"\n{Fore.BLUE}========= {title} =========")
    for k, v in data.items():
        print(f"{Fore.YELLOW}{k}: {Fore.WHITE}{v}")

def print_links(title, links):
    if links:
        print(f"\n{Fore.BLUE}========= {title} =========")
        for l in links:
            print(Fore.CYAN + "- " + l)

def save_output(data):
    with open("final_output.json", "w") as f:
        json.dump(data, f, indent=4)
    print(f"\n{Fore.GREEN}[✓] Saved result in final_output.json")

def recon_guide():
    print(f"""\n{Fore.MAGENTA}========= For more information =========
{Fore.YELLOW}- Save number on WhatsApp and check profile pic, status.
- Check Telegram by syncing contact.
- Use Truecaller manually for identity.
- Check Instagram, Facebook & more by syncing contact.
""")

def main():
    clear_terminal()
    banner("ShaPhone")
    apis = load_api_keys()

    number = input(f"{Fore.CYAN}[?] Enter phone number with country code (e.g., +919876543210): ").strip()

    final_result = {}

    basic = basic_info(number)
    print_section("Basic Info", basic)
    final_result["Basic_Info"] = basic

    nv = numverify_lookup(number, apis.get("numverify_key"))
    print_section("NumVerify Lookup", nv)
    final_result["NumVerify"] = nv

    tw = twilio_lookup(number, apis.get("twilio_sid"), apis.get("twilio_auth"))
    print_section("Twilio Lookup", tw)
    final_result["Twilio"] = tw

    ab = abstract_lookup(number, apis.get("abstract_key"))
    print_section("Abstract API", ab)
    final_result["AbstractAPI"] = ab

    nl = numlookup_io(number, apis.get("numlookup_key"))
    print_section("Numlookup API", nl)
    final_result["NumLookupIO"] = nl

    save_output(final_result)
    recon_guide()

if __name__ == "__main__":
    main()
