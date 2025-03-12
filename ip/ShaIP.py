import argparse
import requests, json
import sys
from sys import argv
import os

parser = argparse.ArgumentParser()
parser.add_argument ("-v", help= "target/host IP address", type=str, dest='target', required=True )
args = parser.parse_args()

fig = Figlet(font='slant')  # You can change the font as desired
ascii_art = fig.renderText("ShaIP")

#colours used
red = '\033[31m'
yellow = '\033[93m'
lgreen = '\033[92m'
clear = '\033[0m'
bold = '\033[01m'
cyan = '\033[96m'

#banner of script
print(Fore.CYAN + ascii_art)
print(f"""{Fore.YELLOW}Peace shouldn't be an option
{Fore.MAGENTA}Script by Shadow
""")

ip = args.target
api = "http://ip-api.com/json/"

try:
        data = requests.get(api+ip).json()
        sys.stdout.flush()
        a = cyan+bold+"[$]"
        b = cyan+bold+"[$]"
        print(red+"<--------------->"+red)
        print (a, "[Victim]:", data['query'])
        print (b, "[ISP]:", data['isp'])
        print (a, "[Organisation]:", data['org'])
        print (b, "[City]:", data['city'])        
        print (a, "[Region]:", data['region'])      
        print (b, "[Longitude]:", data['lon'])       
        print (a, "[Latitude]:", data['lat'])        
        print (b, "[Time zone]:", data['timezone'])
        print (a, "[Zip code]:", data['zip'])
        print(red+"<--------------->"+red)
        print (" "+yellow)

except KeyboardInterrupt:
        print ('Terminating, Bye'+lgreen)
        sys.exit(0)
except requests.exceptions.ConnectionError as e:
        print (red+"[~]"+" check your internet connection!"+clear)
sys.exit(1)
