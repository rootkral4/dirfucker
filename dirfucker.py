import requests
import argparse
import threading
import os
import sys
import signal
import time
from termcolor import colored

def signal_handler(sig, frame):
    print(colored('Exiting please wait while im fucking up those threads bye...', "blue"))
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def max_threads(x):
    x = int(x)
    if x > 100:
        raise argparse.ArgumentTypeError("Maximum Threads is 100")
    return x

parser = argparse.ArgumentParser(description='Web Directory Fucker | Coded By https://github.com/rootkral4')
parser.add_argument('-u', "--url", required=True, help="URL (https://example.com/)", type=str)
parser.add_argument('-w', "--wordlist", required=True, help="Wordlist Path", type=str)

parser.add_argument('-s', "--status_code", required=False, help="Define Custom Status Codes (like 200,204,301)", type=str, default=False)
parser.add_argument('-x', "--extension", required=False, help="With Extension (like .php,.css)", type=str, default=False)
parser.add_argument('-l', "--login", required=False, help="Username", type=str)
parser.add_argument('-p', "--password", required=False, help="Password", type=str)
parser.add_argument('-t', "--threads", required=False, help="Threads Default 30", default=30, type=max_threads)

args = parser.parse_args()
attackurl    = getattr(args,'url')
username     = getattr(args,'login')
password     = getattr(args,'password')
wordlistpath = getattr(args,"wordlist")
status_codes = getattr(args,"status_code")
extension = getattr(args,"extension")
threads      = getattr(args,'threads')

if attackurl[:-1] != "/":
    attackurl += "/"

extensions_list = []
status_code_list = []

global linecount
linecount = 0

if status_codes != False:
    status_codes = status_codes.split(",")
    for status in status_codes:
        status_code_list.append(status)
else:
    status_code_list = [200, 204, 301, 302, 307, 401, 403]

if extension != False:
    extension = extension.split(",")
    for ext in extension:
        extensions_list.append(ext)

with open(wordlistpath, "r", errors='replace') as f:
    wordlist = f.readlines()

def checkdir(url, dirname, statuslist, linecount):
    try:
        r = requests.get(url + dirname, timeout=15, verify=True)
        for status in statuslist:
            if r.status_code == int(status):
                print(colored("[+] " + url + dirname + " - " + str(status), "green"))
    except requests.exceptions.Timeout:
        print(colored("[?] Request Timed Out " + url + dirname, "red"))
    print("[?] " + str(linecount) + "/" +str(len(wordlist)), end="\r")

def checkdirauth(url, dirname, statuslist, username, password, linecount):
    try:
        r = requests.get(url + dirname, timeout=15, verify=True, auth=requests.auth.HTTPBasicAuth(username, password))
        for status in statuslist:
            if r.status_code == int(status):
                print(colored("[+] " + url + dirname + " - " + str(status), "green"))
    except requests.exceptions.Timeout:
        print(colored("[?] Request Timed Out " + url + dirname, "red"))
    print("[?] " + str(linecount) + "/" +str(len(wordlist)), end="\r")

print(colored("""
Coded By rootkral4 | https://github.com/rootkral4
👑 For Real Kings 👑
****************************************
* [*] URL          :{}
* [*] Word Loaded  :{}
* [*] Status Codes :{}
* [*] Extensions   :{}
* [*] Threads      :{}
****************************************
""", "red").format(attackurl, len(wordlist), status_code_list, extensions_list, threads))


if username == None:
    if extension == False:
        for word in wordlist:
            while threading.activeCount() > threads:
                time.sleep(0.1)
            linecount += 1
            threading.Thread(target=checkdir, args=(attackurl, word.strip(), status_code_list, linecount)).start()
    else:
        for word in wordlist:
            while threading.activeCount() > threads:
                time.sleep(0.1)
            linecount += 1
            threading.Thread(target=checkdir, args=(attackurl, word.strip(), status_code_list, linecount)).start()
            for ext in extensions_list:
                while threading.activeCount() > threads:
                    time.sleep(0.1)
                threading.Thread(target=checkdir, args=(attackurl, word.strip()  + ext, status_code_list, linecount)).start()
else:
    if extension == False:
        for word in wordlist:
            while threading.activeCount() > threads:
                time.sleep(0.1)
            linecount += 1
            threading.Thread(target=checkdirauth, args=(attackurl, word.strip(), status_code_list, username, password, linecount)).start()
    else:
        for word in wordlist:
            while threading.activeCount() > threads:
                time.sleep(0.1)
            linecount += 1
            threading.Thread(target=checkdirauth, args=(attackurl, word.strip(), status_code_list, username, password, linecount)).start()
            for ext in extensions_list:
                while threading.activeCount() > threads:
                    time.sleep(0.1)
                threading.Thread(target=checkdirauth, args=(attackurl, word.strip() + ext, status_code_list, username, password, linecount)).start()

print(colored("\n[!] Done !", "yellow"))