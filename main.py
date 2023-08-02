import os
import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.message import EmailMessage


def email(url):
    msg = EmailMessage()
    msg.set_content(f"Change detected on: {url}")

    msg['Subject'] = 'Change Detected'
    msg['From'] = 'nawarkhouri1@gmail.com'
    msg['To'] = 'nawarkhouri1@gmail.com'

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login('nawarkhouri1@gmail.com', os.environ.get('PASSWD'))
    server.send_message(msg)
    server.quit()


def fill(url):
    get_data = requests.get(url)
    soup = BeautifulSoup(get_data.content, 'html.parser')

    return str(soup.find('table'))


def load_urls(file_path="urls.txt"):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


previous_content = {data: fill(data) for data in load_urls()}


while True:
    for url in load_urls():
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        content_to_monitor = str(soup.find('table'))

        if previous_content[url] and content_to_monitor != previous_content[url]:
            email(url)

        previous_content[url] = content_to_monitor

    time.sleep(3600)
