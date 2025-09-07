import os, requests, json
from sqlite3 import paramstyle
from dotenv import load_dotenv

load_dotenv()

GOOGLE_SEARCH_API_KEY = os.getenv('GOOGLE_SEARCH_API_KEY')

params = {
    'key': GOOGLE_SEARCH_API_KEY,
    'cx': os.getenv('SEARCH_ENGINE_ID'),
    'q': 'drop shipping'
}

respose = requests.get('https://www.googleapis.com/customsearch/v1', params=params)

with open('search.json', 'w') as f:
    json.dump(respose.json(), f)

print(respose.json())


