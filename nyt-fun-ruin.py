#!/usr/bin/env python3
import requests
from http import cookiejar
import browser_cookie3
import json
from datetime import date, datetime
import argparse
import subprocess
from bs4 import BeautifulSoup
import time

def get_nyt_s_cookie():
    # Load cookies from Chrome for the nytimes.com domain
    cj = browser_cookie3.chrome(domain_name='nytimes.com')

    # Search for 'NYT-S' cookie
    for cookie in cj:
        if cookie.name == 'NYT-S':
            return {cookie.name: cookie.value}

    raise Exception("NYT-S cookie not found!")

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = f"Not a valid date: '{s}'. Expected format: YYYY-MM-DD"
        raise argparse.ArgumentTypeError(msg)

def send_imessage(recipient, message):
    """Send iMessage via AppleScript"""
    applescript = f'''
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{recipient}" of targetService
        send "{message}" to targetBuddy
    end tell
    '''
    subprocess.run(["osascript", "-e", applescript])

def fetch_url_with_retry(url, cookie, retries=60*24):
    """Fetch a URL with retries in case of failure"""
    for attempt in range(retries):
        try:
            response = requests.get(url, cookies=cookie)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            if attempt < retries - 1:
                print(f"Attempt {attempt + 1} for {url} failed: {e}. Retrying in 5m...")
                time.sleep(300)
            else:
                raise
    return None

def wait_for_url(url, cookie, wait):
    if not wait:
        retries = 1
    else:
        retries = 60 * 24
    return fetch_url_with_retry(url, cookie, retries)

def get_wordle_solution(date_str, cookie, wait):
    """Fetch the Wordle solution from the NYT API"""
    url = f"https://www.nytimes.com/svc/wordle/v2/{date_str}.json"
    resp = wait_for_url(url, cookie, wait)
    return resp.json()['solution'].upper()

def get_mini_solution(date_str, cookie, wait):
    url = f"https://www.nytimes.com/svc/crosswords/v6/puzzle/mini/{date_str}.json"
    resp = wait_for_url(url, cookie, wait)
    puzzle = resp.json()

    height = puzzle["body"][0]["dimensions"]["height"]
    width = puzzle["body"][0]["dimensions"]["width"]
    cells = puzzle["body"][0]["cells"]

    w = 0
    solution=''
    for cell in cells:
        if 'answer' in cell:
            solution += cell["answer"]
        else:
            solution += '.'

        w += 1
        if w >= width:
            solution += '\n'
            w = 0

    return solution

def get_connections_solution(date_str, cookie, wait):
    """Fetch the Connections solution from the NYT API"""
    url = f"https://www.nytimes.com/svc/connections/v2/{date_str}.json"
    resp = wait_for_url(url, cookie, wait)
    solution=''
    for category in resp.json()['categories']:
        solution += f"{category['title']}:\n   "
        for word in category['cards']:
            solution += f"{word['content']},"
        solution = solution.rstrip(',') + '\n'

    return solution

def sbsolver_id(target_date: date) -> int:
    base_date = date(2018, 5, 9)  # The first Spelling Bee puzzle date
    delta_days = (target_date - base_date).days + 1
    return delta_days

def get_spelling_bee_solution(date_str, cookie, wait):
    sbid = sbsolver_id(date_str)
    # URL to scrape (current day's answers)
    url = f"https://www.sbsolver.com/s/{sbid}"

    #print(f"Fetching Spelling Bee solution for {date_str} (ID: {sbid}) from {url}")

    # Fetch the page
    response = wait_for_url(url, cookie, wait)
    #response = requests.get(url)
    #response.raise_for_status()  # Raise an error for bad status codes

    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all links in the solution table
    links = soup.select('table.bee-set a[href^="https://www.sbsolver.com/h/"]')

    words = []
    for link in links:
        # Reconstruct the word from the text and span contents
        parts = []
        for content in link.contents:
            if content.name == 'span':
                parts.append(content.text.strip())
            elif isinstance(content, str):
                parts.append(content.strip())
        word = ''.join(parts)
        words.append(word)

    # Remove duplicates (some words may appear more than once)
    unique_words = list(dict.fromkeys(words))

    return '\n'.join(sorted(unique_words))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--date', '-d',
        type=valid_date,
        default=date.today(),
        help="Date in YYYY-MM-DD format (default: today)"
    )
    parser.add_argument(
        '--games', '-g',
        default="all",
        help="Games to ruin (default: all). Options: mini, wordle, connections, spelling-bee, all"
    )
    parser.add_argument(
        '--recipient', '-r',
        default=None,
        help="iMessage recipient"
    )
    parser.add_argument(
        '--wait', '-w',
        action='store_true',
        default=False,
        help="Wait for the game to be available (default: False)"
    )


    args = parser.parse_args()

    cookie = get_nyt_s_cookie()

    payload = ""
    print("Ruining fun...please wait.")
    if args.games == "all" or args.games == "mini":
        payload += "---------------------------\n"
        payload += f"Mini solution for {args.date}:\n"
        payload += get_mini_solution(args.date, cookie, args.wait) + "\n"
    if args.games == "all" or args.games == "wordle":
        payload += "---------------------------\n"
        payload += f"Wordle solution for {args.date}:\n"
        payload += get_wordle_solution(args.date, cookie, args.wait) + "\n\n"
    if args.games == "all" or args.games == "connections":
        payload += "---------------------------\n"
        payload += f"Connections solution for {args.date}:\n"
        payload += get_connections_solution(args.date, cookie, args.wait) + "\n"
    if args.games == "all" or args.games == "spelling-bee":
        payload += "---------------------------\n"
        payload += f"Spelling bee words for {args.date}:\n"
        payload += get_spelling_bee_solution(args.date, cookie, args.wait)

    print(payload)


    imessage = f"Fun ruined.\n{payload}"
    if args.recipient:
        send_imessage(args.recipient, imessage)
