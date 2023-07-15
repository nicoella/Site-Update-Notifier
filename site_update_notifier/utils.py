from bs4 import BeautifulSoup
import requests
import hashlib
import json # tbd

import asyncio
import aiocron

# hash a given string
def hash_str(str):
    hash_object = hashlib.sha256(str.encode())
    hash_value = hash_object.hexdigest()
    return hash_value

# hash all content within url page
def get_site_hash(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    parsed_html_string = str(soup)
    return hash_str(parsed_html_string)

# send a notification to webhook
def send_notification(webhook, title, description):
    data = {
        "username" : "Site Update Notifier Webhook",
        "embeds" : [
            {
                "description" : description,
                "title" : title
            }
        ]
    }
    try:
        result = requests.post(webhook, json = data)
        result.raise_for_status()
        print("Payload delivered successfully, code {}.".format(result.status_code))
        return True
    except Exception as err:
        print(err)
        return False
    
# check if site was updated    
#def check_update(url, hash, webhook):
#    cur_hash = get_site_hash(url)
#    if cur_hash != hash:
#        print("site updated!!!!")
#        send_notification(webhook, "Site Updated", "Your saved site " + url + " has had updates.")
        
# get all data from backend
# async def get_all_data():
#    data = collection.find()
#    for site in data:
 #       print(site['url']+" "+site['hash']+" "+site['webhook'])
 #       check_update(site['url'], site['hash'], site['webhook'])
    
# check updates
#async def run_task():
#    await aiocron.crontab("*/3 * * * *", func=get_all_data)

#loop = asyncio.get_event_loop()

#loop.run_until_complete(run_task())