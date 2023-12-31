import os
import time
import traceback

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import difflib


def check():
    user_key = os.environ.get('USER_KEY')
    api_token = os.environ.get('API_TOKEN')

    message = f"Up and running. Links on call are: {load_urls()}"

    post_url = "https://api.pushover.net/1/messages.json"

    data = {
        "token": api_token,
        "user": user_key,
        "message": message,
    }
    requests.post(post_url, data=data)


def send_push_notification(url, new):
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        if 'github.com' in domain:
            path_parts = parsed_url.path.strip('/').split('/')
            if path_parts:
                domain = domain + " - " + path_parts[0]
            url = url[0] + " - " + url[1]

        user_key = os.environ.get('USER_KEY')
        api_token = os.environ.get('API_TOKEN')
        message = f"Change detected on: {domain}\nWhat's new: {new}"

        post_url = "https://api.pushover.net/1/messages.json"

        data = {
            "token": api_token,
            "user": user_key,
            "message": message,
        }

        response = requests.post(post_url, data=data)

        if response.status_code != 200:
            write_error_to_file_and_send_notification(response.content)

    except Exception as notify_error:
        error_message = f"send_push_notification\n\nError sending notification for URL {url}: " + str(
            notify_error) + "\n" + traceback.format_exc()
        write_error_to_file_and_send_notification(error_message)


def whats_new(old, new):
    differ = difflib.Differ()
    diffs = list(differ.compare(old, new))
    new = [diff[2:] for diff in diffs if diff.startswith('+ ')]
    return ''.join(new)


def fill(url):
    try:
        get_data = requests.get(url)
        soup = BeautifulSoup(get_data.content, 'html.parser')
        return str(soup.find('table'))
    except Exception as data_error:
        error_message = f"fill\n\nError getting data from URL: {url}.\nError: {str(data_error)}.\n{traceback.format_exc()}"
        write_error_to_file_and_send_notification(error_message)


def load_urls(file_path="urls.txt"):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except Exception as load_url:
        error_message = f"load_urls\n\nError loading url from url.txt.\nError: {load_url}.\n {traceback.format_exc()}"
        write_error_to_file_and_send_notification(error_message)


def write_error_to_file_and_send_notification(error_message):
    with open("error_log.txt", "a") as file:
        file.write(error_message + "\n")

    try:
        user_key = os.environ.get('USER_KEY')
        api_token = os.environ.get('API_TOKEN')
        message = error_message

        post_url = "https://api.pushover.net/1/messages.json"

        data = {
            "token": api_token,
            "user": user_key,
            "message": message,
        }

        response = requests.post(post_url, data=data)

        if response.status_code != 200:
            with open('error_log.txt', 'a') as file:
                file.write(str(response.content) + '\n')
    except Exception as notify_error:
        with open("error_log.txt", "a") as file:
            file.write(str(notify_error) + "\n")

try:
    previous_content = {data: fill(data) for data in load_urls()}
    check()
    while True:
        for url in load_urls():
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            content_to_monitor = str(soup.find('table'))

            if previous_content[url] and content_to_monitor != previous_content[url]:
                new = whats_new(old=previous_content[url], new=content_to_monitor)
                send_push_notification(url, new)

            previous_content[url] = content_to_monitor

        time.sleep(600)
except Exception as error:
    error_message = "while\n\n" + str(error) + "\n" + traceback.format_exc()
    write_error_to_file_and_send_notification(error_message)
