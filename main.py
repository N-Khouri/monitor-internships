import os
import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.message import EmailMessage
import traceback


def email(url):
    try:
        msg = EmailMessage()
        msg.set_content(f"Change detected on: {url}")

        msg['Subject'] = 'Change Detected'
        msg['From'] = 'nawarkhouri1@gmail.com'
        msg['To'] = 'nawarkhouri1@gmail.com'

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('nawarkhouri1@gmail.com', os.environ.get('PASSWD'))
        server.send_message(msg)
        server.quit()
    except Exception as email_error:
        error_message = f"Error sending email for URL {url}: " + str(email_error) + "\n" + traceback.format_exc()
        write_error_to_file_and_email(error_message)


def fill(url):
    try:
        get_data = requests.get(url)
        soup = BeautifulSoup(get_data.content, 'html.parser')
        return str(soup.find('table'))
    except Exception as data_error:
        error_message = f"Error getting data from URL: {url}.\nError: {str(data_error)}.\n{traceback.format_exc()}"
        write_error_to_file_and_email(error_message)


def load_urls(file_path="urls.txt"):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except Exception as load_url:
        error_message = f"Error loading url from url.txt.\nError: {load_url}.\n {traceback.format_exc()}"
        write_error_to_file_and_email(error_message)


def write_error_to_file_and_email(error_message):
    with open("error_log.txt", "a") as file:
        file.write(error_message + "\n")

    try:
        msg = EmailMessage()
        msg.set_content(error_message)
        msg['Subject'] = 'Error in Script'
        msg['From'] = 'nawarkhouri1@gmail.com'
        msg['To'] = 'nawarkhouri1@gmail.com'
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('nawarkhouri1@gmail.com', os.environ.get('PASSWD'))
        server.send_message(msg)
        server.quit()
    except Exception as email_error:
        with open("error_log.txt", "a") as file:
            file.write(str(email_error) + "\n")


try:
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
except Exception as error:
    error_message = str(error) + "\n" + traceback.format_exc()
    write_error_to_file_and_email(error_message)
