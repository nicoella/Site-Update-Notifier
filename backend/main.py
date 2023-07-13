from bs4 import BeautifulSoup
import requests
import hashlib
import json # tbd

import asyncio
import aiocron

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
from bson.objectid import ObjectId

from config import config # Place your Mongo URI in a config.py file

app = Flask(__name__)
app.config["MONGO_URI"] = config["MONGO_URI"] 
mongo = PyMongo(app)
mongo_client = MongoClient(config["MONGO_URI"])

db = mongo_client["Cluster0"] # Update with your Cluster name

collection = db["data"] # Update with your Collection name

# base for api
@app.route("/api/")
def welcome():
    return "api is running"

# update database POST request
@app.route("/api/data", methods=["POST"])
def insert_data():
    print(request.json)
    site = request.json.get("site")
    webhook = request.json.get("webhook")
    hash_value = get_site_hash(site)
    hash_id = hash_str(site+" "+webhook)
    insert_result = collection.insert_one({"_id": hash_id, "site":site, "hash":hash_value, "webhook":webhook}).acknowledged
    if not insert_result:
        return {"status": "bad insert"}
    if not send_notification(webhook, "Webhook Added", "Your webhook has been added for the site "+site+". Update notifications will be sent here."):
        collection.delete_one({"_id": hash_id})        
        return {"status": "bad webhook"}
    return {"status": "success"}

# check database status
@app.route("/api/ping")
def ping_mongodb():
    try:
        mongo_client.admin.command('ping')
        return "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        return e

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
def check_update(url, hash, webhook):
    cur_hash = get_site_hash(url)
    if cur_hash != hash:
        print("site updated!!!!")
        send_notification(webhook, "Site Updated", "Your saved site " + url + " has had updates.")
        
# get all data from backend
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