import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import csv

# Load environment variables from .env file
load_dotenv()

# Retrieve email and password from environment variables
EMAIL = os.environ.get('pcoemail')
PASSWORD = os.environ.get('pcopass')
FORM_ID = '9041'  # The ID of the Form

# URL for downloading the form submissions
SCRAPEURL = 'https://people.planningcenteronline.com/forms/' + FORM_ID + '/submissions/export.csv'

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.99 Safari/537.36'
}

# Initialize login data with placeholders for authenticity_token and utf8
login_data = {
    'utf8': None,
    'email': EMAIL,
    'password': PASSWORD,
    'authenticity_token': None
}

with requests.Session() as s:
    # Get the login page to retrieve the authenticity_token and utf8 values
    url = 'https://accounts.planningcenteronline.com/login'
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    login_data['authenticity_token'] = soup.find('input', attrs={'name': 'authenticity_token'})['value']
    login_data['utf8'] = soup.find('input', attrs={'name': 'utf8'})['value']

    # Log in to the site
    r = s.post(url, data=login_data, headers=headers)

    # Download the CSV file with form submissions
    page = s.get(SCRAPEURL)
    csv_file = page.content.decode('utf-8')

    # Process the CSV file
    csv_reader = csv.reader(csv_file.splitlines(), delimiter=',')
    line_count = 0
    for row in csv_reader:
        print(row)
        line_count += 1
