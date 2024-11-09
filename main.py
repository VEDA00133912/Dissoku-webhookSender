from bs4 import BeautifulSoup
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

h = {
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 Chrome/130.0.0.0 Safari/537.36'
}

def send_to_webhook(message):
    payload = {
        'content': message 
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)

for i in range(300):
    r = requests.get(f'https://dissoku.net/ja/servers?page={i}', headers=h).text
    al = BeautifulSoup(r, 'html.parser').find_all('a', class_="join-btn")
    
    for link in al:
        url = requests.get(link.get("href") + "/", headers=h, allow_redirects=False)
        location = url.headers.get('location')
        
        if location != None:
            send_to_webhook(location)
