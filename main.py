import os
import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.message import EmailMessage

urls_to_monitor = [
    "https://www.levels.fyi/internships/?track=Software%20Engineer&timeframe=Summer%20-%202024",
    "https://github.com/SimplifyJobs/Summer2024-Internships",
]


def fill(url):
    get_data = requests.get(url)
    soup = BeautifulSoup(get_data.content, 'html.parser')

    return str(soup.find('table'))


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


previous_content = {data: fill(data) for data in urls_to_monitor}

while True:
    for url in urls_to_monitor:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        content_to_monitor = str(soup.find('table'))

        if previous_content[url] and content_to_monitor != previous_content[url]:
            email(url)

        previous_content[url] = content_to_monitor

    time.sleep(3600)
