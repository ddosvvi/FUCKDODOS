# FUCKDOS

> a high-frequency HTTP request sending tool designed for testing and suppression purposes. It can send random HTTP requests (GET, POST, PUT, DELETE) to specified target URLs
>
> UPDATE NEW METHODS
> - FUCKDOS
> - FUCKHTTP
>
> MAKE FROM INDONESIA | CREDIT BY VINNOTSEPUH


## Installation on Linux 

Install Python 3

```bash
sudo apt update
sudo apt install python3 python3-pip
cd FUCKDODOS/fuck
pip install -r requirements.txt
python3 fuckdos.py
```

## Installation on Termux

Install Python 3

```bash
pkg update
pkg install python
cd FUCKDODOS/fuck
pip install -r requirements.txt
python fuckdos.py
```

## List of Features Already Added
```bash
[+] HTTP Flood (DDoS): Sends a large number of HTTP requests to the target to overwhelm the server.
[+] Randomized User-Agent: Each request uses a different User-Agent to mimic traffic from various devices.
[+] Dynamic Path Generation: Generates random paths for each request to make detection harder.
[+] Randomized Query Parameters: Adds random query parameters to each request.
[+] Multi-Threading: Uses ThreadPoolExecutor to send requests simultaneously with adjustable thread count.
[+] Request Rate Control: Controls the number of requests per second to avoid being blocked by firewalls or security systems.
[+] IP Spoofing: Uses the `X-Forwarded-For` header with random IPs to hide the original identity.
[+] Traffic Monitoring: Displays real-time statistics like total requests and requests per second.
[+] Error Handling: Handles errors such as timeouts, connection errors, and invalid URLs more effectively.
[+] Custom Headers: Adds custom headers to make requests appear more natural.
[+] Logging System: Logs all attack activities into a file (`http_flood.log`) for further analysis.
[+] Colorful Output: Uses the `colorama` library to display colored output in the terminal.
[+] Argument Parsing: Uses `argparse` to accept command-line inputs like target URLs, thread count, and request rate.
```
