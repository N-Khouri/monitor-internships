# Internship Monitor

Internship Monitor is a Python script designed to monitor specified web pages for changes in their content, such as new internship postings. When a change is detected, the script sends an email notification with the details.

## Features

- Monitors a list of URLs for changes.
- Sends push notifications to your phone when changes are detected.
- Allows dynamic updating of monitored URLs through an external text file.
- Utilizes BeautifulSoup to parse HTML content.

## Requirements

- Python 3.x
- BeautifulSoup
- requests
- Pushover Application - API key & User Key

## Installation

1. Clone the repository or download the code to your local machine.
2. Install the required packages by running:
    ```bash
   pip install beautifulsoup4 requests

## Usage

1. Add the URLs you want to monitor to a file named urls.txt, with one URL per line.
2. Set up the push notification configuration within the script, including the API key and user key. Both should be stored as environment variables named API_TOKEN and USER_KEY, respectively.
3. Run the script:
    ```bash
   python main.py
   
## Configuration
- URLs: The URLs to be monitored should be added to the urls.txt file.
- Notification: Modify the notification function in the script to configure the Pushover settings and recipient details.

## Notes
- The script checks the URLs for changes every 3600 seconds (1 hour). You can adjust this interval as needed.
- Ensure that the web pages you are monitoring use a table structure that is compatible with the script's parsing logic.

## License
This project is open-source and available under the MIT License.

## Support and Contribution
Feel free to open an issue or submit a pull request if you have any questions, find a bug, or want to contribute to the project.

## Disclaimer
Please use this script responsibly and ensure that you have the right to access and monitor the web pages you are targeting.