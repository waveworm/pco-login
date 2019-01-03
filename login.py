import requests
from bs4 import BeautifulSoup
import os

""" Your login information below. It's probably best to store this in environment variables."""
EMAIL = 'email@example.com'
PASSWORD = 'password'

""" Uncomment below and comment out above if you're using environment variables"""
# EMAIL = os.environ.get('pcoemail')
# PASSWORD = os.environ.get('pcopass')

""" Internal URL that requires user to be logged in"""
SCRAPEURL = 'https://people.planningcenteronline.com/forms/368/submissions'

"""Here is where we setup headers to make it look like a browser"""
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.99 Safari/537.36'
}

"""This is a dictionary for storing the login post request. Notice 'authenticity_token' is set to None."""
login_data = dict(utf8=None, # The site wants this field probably for localization. We'll populate this below.
                  email=EMAIL,
                  password=PASSWORD,
                  authenticity_token=None) # We'll populate this below after we initilize the session.

with requests.Session() as s:
    """Open a requests session, Store the authenticity_token in the login_data dictionary, make post request with dictionary"""
    url = 'https://accounts.planningcenteronline.com/login' # Login URL
    r = s.get(url, headers=headers) # This is where we make the first request to generate an authenticity_token
    soup = BeautifulSoup(r.content, 'html.parser') # We're using Beautiful Soup to scrape the token form the page source
    """Here we are populating login_data dictionary witht the scraped authenticity_token"""
    login_data['authenticity_token'] = soup.find('input', attrs={'name': 'authenticity_token'})['value']
    """The login also wants a field called utf8 and a value from the site. This is probably for localization."""
    login_data['utf8'] = soup.find('input', attrs={'name': 'utf8'})['value']
    """Finally we submit the post request with the same 's' session passing the url, login_data, and headers for user agent."""
    r = s.post(url, data=login_data, headers=headers)

    """Now we can scrape any url that requires a user to be logged in as long as we use the same session object 's' """
    page = s.get(SCRAPEURL)
    """ Add your own beautiful soup code below"""
    print(page.content)
