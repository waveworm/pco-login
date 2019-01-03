# pco-login
Boilerplate to login to Planning Center Online with python requests


Here's a broad overview of the process of figuring out how to login to a page using python.
1. Use inspect tool in chrome dev tools to find the names of fields used for the login. You are focusing on the field names because you need to submit a dictionary with those names as the key fields and your data as the values.

Right click the login page and click inspect. 
Click the network tab and then do the login normally through the page.  
In the list in the network tab look for the post request that performed the login. 
It’s usually a post to /login or /login/auth or something like that. 
Scroll to the bottom of that request and you’ll be able to see all the information that is sent to complete the login.  
Usually there are at least 3 things: User, Password, csftoken. Sometimes theres more stuff that the server expects.

You can also see these fields in the cookies tab, but the cookies tab will have lots of other fields that aren't needed for login.
Each site will name these login fields their own way so user may be username or email or anything else. The cross site forgery token could be csftoken or 'authenticity_token' or 'my_amazing_middle_ware'. Just make note of the field names.
In your script you need to start a session and get the cross site forgery token.  This is a signed token that lets the server know you are not doing a cross site scripting attack.  You’ll need to submit that token with your username and password for the login to work. This is usually what trips people up along with the diverse names of the login fields.

2. Make a login_data dictionary with all the login fields. Put your credentials in the dictionary values, but set the token field to None. You may also need to make a headers dictionary with the user agent information.
3. Use requests to start a session and grab the csftoken. You can scrape this using scrappy or Beautiful Soup or even pull it from the cookies.
4. Add the token you just got to the login_data dictionary replacing None with the actual token.
5. Use the same session object to make the post request and pass the login_data dictionary.
    r = s.post(url, data=login_data, headers=headers)
6. If all this worked you should get a 200 status_code.
    print(r.status_code)
7. Now you can use that same session object 's' to load pages that require authentication and pass those to Scrappy or BeautifulSoup

Usually it’s the token that messes people up. The token changes every session. So if you open a session and get the token and then open a new session to post and use the other token it won’t work.  You have to open a session with a get request, read the token from the cookies and then in the same session make a post to the login url.  Each site has it's own required fields for logging in. You're going to have to experiment to get it right.
Here’s a demo of how to do this for a site our church uses:
https://github.com/pastorhudson/pco-login/blob/master/login.py
