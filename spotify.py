import json
import spotipy
import webbrowser
import os

username = ""
clientID = os.getenv("SP_CLIENT_ID")
clientSecret = os.getenv("SP_CLIENT_SECRET")
redirect_uri = 'http://google.com/callback/'

print(username, clientID, clientSecret, redirect_uri)