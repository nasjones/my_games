from dotenv import load_dotenv
from threading import Timer
from models import Platforms
import os
import requests
import random

load_dotenv()

GB_key = os.environ.get("gamebomb_key")
CLIENT_ID = os.environ.get("client_id")
CLIENT_SECRET = os.environ.get("client_secret")

BASE_URL_SEARCH = "https://www.giantbomb.com/api/games/?api_key={key}&offset={offset}&format=json&filter={name},{platform}&field_list=deck,description,guid,image,name"

BASE_URL_GAME = "https://www.giantbomb.com/api/game/{id}/?api_key={key}&format=json"

SIMILAR_URL = "https://api.igdb.com/v4/games"

AUTH_ENDPOINT = f"https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials"

auth_state = False
token = ""


def search_api(name, platform_id, page):
    """Function used to reach the search portion of the video game api"""
    # Just a failsafe if the user managed to submit an empty string to return none
    if name:
        name = f"name:{name}"
    else:
        return(None)

    # Set the platform id for the api call
    if(platform_id == 0):
        platform = ""
    else:
        platform = f"platforms:{platform_id}"

    # Set the offset number for the api call to get all results by separating into pages
    if (page > 1):
        offset = (page-1)*100
    else:
        offset = 0

    endpoint = BASE_URL_SEARCH.format(
        key=GB_key, platform=platform, name=name, offset=offset)
    r = requests.get(endpoint, headers={'user-agent': 'Nas-test-app'})
    data = r.json()
    return(data)


def single_game(id):
    """function used to reach the singular video game portion of the video game api"""
    endpoint = BASE_URL_GAME.format(
        key=GB_key, id=id)
    r = requests.get(endpoint, headers={'user-agent': 'Nas-test-app'})
    data = r.json()
    return(data)


def similar_games(query):
    """function used to reach the similar video games api"""
    global auth_state
    global token
    if not auth_state:
        token, expiration = auth()
        t = Timer(expiration, unauth)
        t.start()

    payload = f'fields similar_games.name; where name = \"{query}\";'

    r = requests.request("POST", url=SIMILAR_URL,
                         headers={
                             'Client-ID': CLIENT_ID,
                             'Authorization': f"Bearer {token}"
                         },
                         data=payload
                         )

    json_data = r.json()[0] if r.status_code == 200 and r.json() else {
        "similar_games": []}
    data = json_data["similar_games"]
    output = []
    if data:
        output = random.sample(data, 5)

    return(output)


def auth():
    """Function used to get new credentials"""
    global auth_state
    r = requests.post(url=AUTH_ENDPOINT)
    data = r.json()
    auth_state = True
    return data["access_token"], data["expires_in"]


def unauth():
    global auth_state
    auth_state = False
