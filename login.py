import requests
from bs4 import BeautifulSoup
import os

""" Your login information below. It's probably best to store this in environment variables."""
EMAIL = 'email@example.com'
PASSWORD = 'password'
""" Internal URL """
SCRAPEURL = 'https://people.planningcenteronline.com/forms/368/submissions'

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.99 Safari/537.36'
}

login_data = dict(utf8=None,
                  email=EMAIL,
                  password=PASSWORD,
                  authenticity_token=None)

with requests.Session() as s:
    url = 'https://accounts.planningcenteronline.com/login'
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    login_data['authenticity_token'] = soup.find('input', attrs={'name': 'authenticity_token'})['value']
    login_data['utf8'] = soup.find('input', attrs={'name': 'utf8'})['value']
    r = s.post(url, data=login_data, headers=headers)
    if r.status_code == 200:
        print('Successfully Logged into Planning Center!\n\n')
    else:
        print('Something went wrong. Please check the url, username, and password\n\n')

    """ The page you actually want to scrape"""
    page = s.get(SCRAPEURL)
    """ Change this to parse the page you want."""
    print(page.content)
