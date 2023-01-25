from dotenv import load_dotenv
from models import Platforms
import os
import requests
import random

load_dotenv()

GB_key = os.environ.get("gamebomb_key")
TD_key = os.environ.get("tastedive_key")

BASE_URL_SEARCH = "https://www.giantbomb.com/api/games/?api_key={key}&offset={offset}&format=json&filter={name},{platform}&field_list=deck,description,guid,image,name"

BASE_URL_GAME = "https://www.giantbomb.com/api/game/{id}/?api_key={key}&format=json"

BASE_URL_SIMILAR = "https://tastedive.com/api/similar?q={query}&type=game&limit=50&k={key}"


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
    endpoint = BASE_URL_SIMILAR.format(
        key=TD_key, query=query)

    r = requests.get(endpoint, headers={'user-agent': 'Nas-test-app'})
    data = r.json()["Similar"]["Results"] if r.status_code == 200 else None
    output = []
    if data:
        output = random.sample(data, 6)

    return(output)
