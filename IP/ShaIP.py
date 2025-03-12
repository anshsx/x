import requests, json
import sys
import os
from pyfiglet import Figlet
from colorama import Fore, Style, init

init()

fig = Figlet(font='slant')  # You can change the font
ascii_art = fig.renderText("ShaIP")

# Colours
red = '\033[31m'
yellow = '\033[93m'
lgreen = '\033[92m'
clear = '\033[0m'
bold = '\033[01m'
cyan = '\033[96m'

# Banner
print(Fore.CYAN + ascii_art)
print(f"""{Fore.YELLOW}Peace shouldn't be an option
{Fore.MAGENTA}Script by Shadow
""")

# Ask for IP input
ip = input(f"{Fore.CYAN}[?] Enter Target IP: {Fore.RESET}")

api = "http://ip-api.com/json/"

try:
    data = requests.get(api + ip).json()
    sys.stdout.flush()
    a = cyan + bold + "[$]"
    b = cyan + bold + "[$]"
    print(red + "<--------------->" + red)
    print(a, "[Victim]:", data['query'])
    print(b, "[ISP]:", data['isp'])
    print(a, "[Organisation]:", data['org'])
    print(b, "[City]:", data['city'])
    print(a, "[Region]:", data['region'])
    print(b, "[Longitude]:", data['lon'])
    print(a, "[Latitude]:", data['lat'])
    print(b, "[Time zone]:", data['timezone'])
    print(a, "[Zip code]:", data['zip'])
    print(red + "<--------------->" + red)
    print(" " + yellow)

except KeyboardInterrupt:
    print('Terminating, Bye' + lgreen)
    sys.exit(0)
except requests.exceptions.ConnectionError:
    print(red + "[~] Check your internet connection!" + clear)
    sys.exit(1)
