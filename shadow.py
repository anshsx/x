import os
import json
import requests
import shutil
import time
from pyfiglet import figlet_format
from termcolor import colored

# --- CONFIG ---
REPO_URL = "https://github.com/anshsx/x"  # <-- Replace with actual repo
RAW_VERSION_URL = "https://raw.githubusercontent.com/anshsx/x/main/version.txt"
LOCAL_VERSION_FILE = "version.txt"
TOOLS_JSON_PATH = "data.json"
REPO_NAME = "ShadowX"

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def banner():
    print(colored(figlet_format("SHADOW X"), "cyan"))
    print(colored(">> The Ultimate Recon Toolkit for Termux/Kali <<\n", "green"))

def load_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return None
    with open(LOCAL_VERSION_FILE, "r") as f:
        return f.read().strip()

def fetch_latest_version():
    try:
        response = requests.get(RAW_VERSION_URL)
        if response.status_code == 200:
            return response.text.strip()
    except:
        pass
    return None

def update_tool():
    print(colored("\n[!] A new version is available. Updating Shadow X...", "yellow"))
    print(colored("    Please wait... ", "cyan"))
    
    # Simulate loader
    for i in range(3):
        print("." * (i + 1))
        time.sleep(1)

    os.chdir("..")
    if os.path.exists(REPO_NAME):
        shutil.rmtree(REPO_NAME)

    os.system(f"git clone {REPO_URL}")
    print(colored("\n[+] Update complete! Run the tool again.", "green"))
    exit()

def load_tools():
    if not os.path.exists(TOOLS_JSON_PATH):
        print(colored("[!] data.json not found!", "red"))
        exit()
    with open(TOOLS_JSON_PATH, "r") as f:
        return json.load(f)

def show_tools(tools):
    print(colored("\nAvailable Attack Tools:\n", "magenta"))
    for idx, tool in enumerate(tools, start=1):
        print(f"{idx}. {tool['name']}")
    print(f"{len(tools)+1}. Exit")

def run_tool(tools):
    try:
        choice = int(input("\nEnter your choice: "))
        if choice == len(tools) + 1:
            print(colored("Goodbye!", "cyan"))
            exit()
        tool = tools[choice - 1]
        os.system(tool["run"])
    except (IndexError, ValueError):
        print(colored("[!] Invalid choice. Try again.", "red"))
        run_tool(tools)

def main():
    clear()
    banner()

    local_version = load_local_version()
    latest_version = fetch_latest_version()

    if latest_version and local_version != latest_version:
        update_tool()

    tools = load_tools()
    show_tools(tools)
    run_tool(tools)

if __name__ == "__main__":
    main()
