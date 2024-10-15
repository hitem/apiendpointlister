#!/usr/bin/env python3

# # # # # # # # # # # # # # # # # # # # # # # #
# made by hitemSec
# github: https://github.com/hitem
# mastodon: @hitem@infosec.exchange 
# # # # # # # # # # # # # # # # # # # # # # # #

import requests
import json
import argparse
from urllib.parse import urlparse
from collections import defaultdict
from colorama import Fore, Style, init

init(autoreset=True)

def interpolate_color(color1, color2, factor):
    """Interpolate between two RGB colors."""
    return [int(color1[i] + (color2[i] - color1[i]) * factor) for i in range(3)]

def rgb_to_ansi(r, g, b):
    """Convert RGB to ANSI color code."""
    return f'\033[38;2;{r};{g};{b}m'

def print_logo_and_instructions():
    logo = """
  ▄ .▄▪  ▄▄▄▄▄▄▄▄ .• ▌ ▄ ·. .▄▄ · ▄▄▄ . ▄▄·  
 ██▪▐███ •██  ▀▄.▀··██ ▐███▪▐█ ▀. ▀▄.▀·▐█ ▌▪ 
 ██▀▐█▐█· ▐█.▪▐▀▀▪▄▐█ ▌▐▌▐█·▄▀▀▀█▄▐▀▀▪▄██ ▄▄ 
 ██▌▐▀▐█▌ ▐█▌·▐█▄▄▌██ ██▌▐█▌▐█▄▪▐█▐█▄▄▌▐███▌ 
 ▀▀▀ ·▀▀▀ ▀▀▀  ▀▀▀ ▀▀  █▪▀▀▀ ▀▀▀▀  ▀▀▀ ·▀▀▀  
    """
    colors = [
        (255, 0, 255),  # Purple
        (0, 0, 255)     # Blue
    ]

    num_colors = len(colors)
    rainbow_logo = ""
    color_index = 0
    num_chars = sum(len(line) for line in logo.split("\n"))
    for char in logo:
        if char != " " and char != "\n":
            factor = (color_index / num_chars) * (num_colors - 1)
            idx = int(factor)
            next_idx = min(idx + 1, num_colors - 1)
            local_factor = factor - idx
            color = interpolate_color(colors[idx], colors[next_idx], local_factor)
            rainbow_logo += rgb_to_ansi(*color) + char
            color_index += 1
        else:
            rainbow_logo += char

    instructions = f"""
    {rainbow_logo}{Style.RESET_ALL}
    {Fore.LIGHTBLACK_EX}Improve your reconnaissance by {Fore.RED}hitemSec{Style.RESET_ALL}
    {Fore.LIGHTBLACK_EX}How-To: {Fore.YELLOW}python3 apiendpointlister.py -h{Style.RESET_ALL}

    {Fore.GREEN}APIendpointlister - Usage Instructions{Style.RESET_ALL}
    {Fore.YELLOW}--------------------------------------{Style.RESET_ALL}
    This tool lists all API Endpoints available in swagger.json (openAPI)
    
    {Fore.YELLOW}Usage:{Style.RESET_ALL}
    python3 apiendpointlister.py [OPTIONS]
    
    {Fore.YELLOW}Options:{Style.RESET_ALL}
    -u, --urls          Path to the URL list file
    -o, --output        Output file for results
    
    {Fore.YELLOW}Examples:{Style.RESET_ALL}
    Check endpoints from a URL list:
        python3 apiendpointlister.py -u urllist.txt -o output.txt

    {Fore.GREEN}Happy Recon!{Style.RESET_ALL}
    """
    print(instructions)

def fetch_swagger_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"[{Fore.GREEN}{response.status_code}{Style.RESET_ALL}] {url}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[{Fore.RED}ERROR{Style.RESET_ALL}] {url} - {e}")
        return None

def extract_endpoints(swagger_json, base_url):
    if not swagger_json or 'paths' not in swagger_json:
        return []
    
    endpoints = []
    for path in swagger_json['paths'].keys():
        endpoints.append(base_url + path)
    return endpoints

from urllib.parse import urlparse, urlunparse

def process_urls(input_file, output_file):
    with open(input_file, 'r') as file:
        urls = file.readlines()
    
    all_endpoints = []

    for url in urls:
        url = url.strip()
        
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = 'https://' + url
            parsed_url = urlparse(url)
        
        base_url = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_url)
        
        swagger_json = fetch_swagger_json(url)
        if swagger_json:
            endpoints = extract_endpoints(swagger_json, base_url)
            all_endpoints.extend(endpoints)
    
    all_endpoints = sorted(all_endpoints)

    with open(output_file, 'w') as file:
        for endpoint in all_endpoints:
            file.write(endpoint + '\n')

if __name__ == "__main__":
    print_logo_and_instructions()
    
    parser = argparse.ArgumentParser(description="Extract endpoints from Swagger/OpenAPI JSON files.")
    parser.add_argument('-u', '--urls', required=True, help="File containing list of Swagger/OpenAPI JSON URLs")
    parser.add_argument('-o', '--output', required=True, help="File to save the extracted apiendpoints")
    
    args = parser.parse_args()
    
    process_urls(args.urls, args.output)