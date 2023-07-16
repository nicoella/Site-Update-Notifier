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
        # print("Payload delivered successfully, code {}.".format(result.status_code))
        return True
    except Exception as err:
        print(err)
        return False
    