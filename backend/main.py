from bs4 import BeautifulSoup
import requests
import hashlib
import json # tbd

import asyncio
import aiocron

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

from pymongo.mongo_client import MongoClient

from config import config # Place your Mongo URI in a config.py file

app = Flask(__name__)
app.config["MONGO_URI"] = config["MONGO_URI"] 
mongo = PyMongo(app)
mongo_client = MongoClient(config["MONGO_URI"])

db = mongo_client["Cluster0"] # Update with your Cluster name

collection = db["data"] # Update with your Collection name

@app.route("/api/")
def welcome():
    return "api is running"

@app.route("/api/data", methods=["POST"])
def insert_data():
    print(request.json)
    site = request.json.get("site")
    webhook = request.json.get("webhook")
    hash_value = get_site_hash(site)
    if not collection.insert_one({"site":site, "hash":hash_value, "webhook":webhook}).acknowledged:
        return {"status": "bad insert"}
    if not send_notification(webhook, "Webhook Added", "Your webhook has been added for the site "+site+". Update notifications will be sent here."):
        print("error")
        return {"status": "bad webhook"}
    return {"status": "success"}

@app.route("/api/ping")
def ping_mongodb():
    try:
        mongo_client.admin.command('ping')
        return "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        return e

def get_site_hash(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    parsed_html_string = str(soup)
    hash_object = hashlib.sha256(parsed_html_string.encode())
    hash_value = hash_object.hexdigest()
    return hash_value


def send_notification(webhook, title, description):
    data = {
        "username" : "Site Update Notifier Webhook",
        "embeds": {
            "description" : description,
            "title" : title
        }
    }
    try:
        result = requests.post(webhook, json = data)
        result.raise_for_status()
        print("Payload delivered successfully, code {}.".format(result.status_code))
        return True
    except Exception as err:
        print(err)
        return False
        
def check_update(url, hash, webhook):
    cur_hash = get_site_hash(url)
    if cur_hash != hash:
        print("site updated!!!!")
        send_notification(webhook, "Site Updated", "Your saved site " + url + " has had updates.")
        
async def get_all_data():
    data = collection.find()
    for site in data:
        print(site['url']+" "+site['hash']+" "+site['webhook'])
        check_update(site['url'], site['hash'], site['webhook'])
    
# run backend    
if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
    
# check updates
#async def run_task():
#    await aiocron.crontab("*/3 * * * *", func=get_all_data)

#loop = asyncio.get_event_loop()

#loop.run_until_complete(run_task())