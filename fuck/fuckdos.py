import requests
import random
import time
import logging
import sys
import socket
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore
import argparse

fuck = "\033[38;5;118m"
white = "\033[97m"
red = "\033[38;5;196m"
green = "\033[38;5;34m"
clear = "\033[0m"
pur = "\033[38;5;129m"

init(autoreset=True)

# Konfigurasi logging
logging.basicConfig(
    filename="http_flood.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    print(f'''{pur}    
  █████▒█    ██  ▄████▄   ██ ▄█▀▓█████▄  ▒█████    ██████ 
▓██   ▒ ██  ▓██▒▒██▀ ▀█   ██▄█▒ ▒██▀ ██▌▒██▒  ██▒▒██    ▒ 
▒████ ░▓██  ▒██░▒▓█    ▄ ▓███▄░ ░██   █▌▒██░  ██▒░ ▓██▄   
░▓█▒  ░▓▓█  ░██░▒▓▓▄ ▄██▒▓██ █▄ ░▓█▄   ▌▒██   ██░  ▒   ██▒
░▒█░   ▒▒█████▓ ▒ ▓███▀ ░▒██▒ █▄░▒████▓ ░ ████▓▒░▒██████▒▒
 ▒ ░   ░▒▓▒ ▒ ▒ ░ ░▒ ▒  ░▒ ▒▒ ▓▒ ▒▒▓  ▒ ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░
 ░     ░░▒░ ░ ░   ░  ▒   ░ ░▒ ▒░ ░ ▒  ▒   ░ ▒ ▒░ ░ ░▒  ░ ░
 ░ ░    ░░░ ░ ░ ░        ░ ░░ ░  ░ ░  ░ ░ ░ ░ ▒  ░  ░  ░  
          ░     ░ ░      ░  ░      ░        ░ ░        ░  
                ░                ░                                                                                            
    {clear}
╔═════════════════════════════════════════════════════╗
║ {fuck}*{clear} Telegram  {fuck}:{clear}   https://t.me/VinNotSepuh            ║
║ {fuck}*{clear} version   {fuck}:{clear}   2.1                                 ║
║ {fuck}*{clear} Created   {fuck}:{clear}   VinNotSepuh                         ║
╚═════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════╗
║ {fuck}[{clear}description{fuck}]{clear} Alat HTTP Flood Canggih dengan Fitur Tambahan           ║  
║                                                                       ║
║ {red}[{clear} INFO {red}]{clear} Tools ini masih beta                                         ║   
╚═══════════════════════════════════════════════════════════════════════╝ 

╔═════════════════════════════════════════════════════════════════════════════╗
║ {fuck}[{clear}NEW{fuck}]{clear} METHODS FUCK                                                          ║  
║                                                                             ║
║ {red}[{clear} FUCKDOS {red}]{clear} Sedang Update | COMING SOON                                     ║
║ {red}[{clear} FUCKHTTP {red}]{clear} No SSL Target | Sedang Update | COMING SOON                    ║
║ {red}[{clear} FUCKBITCH {red}]{clear} No SSL Target | Sedang Update | COMING SOON                   ║
║                                                                             ║
║ {red}[{clear} USAGE FUCKDOS {red}]{clear} fuckdos.py example.com -t 20 -r 50                        ║
║ {red}[{clear} USAGE FUCKHTTP {red}]{clear} fucKhttp.py example.com time req thread proxy.txt        ║
║ {red}[{clear} USAGE FUCKBITCH {red}]{clear} fuckbitch.py                                            ║          
╚═════════════════════════════════════════════════════════════════════════════╝ 

''')