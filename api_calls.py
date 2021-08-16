from dotenv import load_dotenv
import os
import requests
from models import Platforms
load_dotenv()

token = os.environ.get("api_token")
BASE_URL = "https://www.giantbomb.com/api/games/?api_key={token}&format=json&filter={name},{platform}"


def search_api(query, platform_id, page=0):
    if(platform_id == 0):
        platform = ""
    else:
        platform = f"platforms:{platform_id}"

    name = f"name:{query}"

    endpoint = BASE_URL.format(token=token, platform=platform, name=name)
    r = requests.get(endpoint, headers={'user-agent': 'Nas-test-app'})
    data = r.json()
    return(data)
