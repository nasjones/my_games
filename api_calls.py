from dotenv import load_dotenv
from models import Platforms
import os
import requests
import random

load_dotenv()

GB_key = os.environ.get("gamebomb_key")
TD_key = os.environ.get("tastedive_key")
BASE_URL_SEARCH = "https://www.giantbomb.com/api/games/?api_key={key}&offset={offset}&format=json&filter={name},{platform}"

BASE_URL_GAME = "https://www.giantbomb.com/api/game/{id}/?api_key={key}&format=json"

BASE_URL_SIMILAR = "https://tastedive.com/api/similar?q={name}&type=game&limit=30&k={key}"


def search_api(name, platform_id, page):
    if name:
        name = f"name:{name}"
    else:
        return(None)

    if(platform_id == 0):
        platform = ""
    else:
        platform = f"platforms:{platform_id}"
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
    endpoint = BASE_URL_GAME.format(
        key=GB_key, id=id)
    r = requests.get(endpoint, headers={'user-agent': 'Nas-test-app'})
    data = r.json()
    return(data)


def similar_games(name):
    endpoint = BASE_URL_SIMILAR.format(
        key=TD_key, name=name)
    r = requests.get(endpoint, headers={'user-agent': 'Nas-test-app'})
    data = r.json()["Similar"]["Results"]
    output = []
    if data:
        output = random.sample(data, 5)

    return(output)
