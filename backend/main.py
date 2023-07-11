from bs4 import BeautifulSoup
import requests
import hashlib
import json

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
    return "api"

@app.route("/api/data", methods=["POST"])
def insert_data():
    site = request.form.get("site")
    webhook = request.form.get("webhook")
    hash_value = get_site_hash(site)
    collection.insert({"site":site, "hash":hash_value, "webhook":webhook})
    send_notification(webhook, "Webhook Added", "Your webhook has been added for the site "+site+". Update notifications will be sent here.")
    return "test"

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


def send_notification(webhook_url, title, description):
    data = {
        "username" : "Site Update Notifier Webhook"
    }
    data["embeds"] = [
        {
            "description" : description,
            "title" : title
        }
    ]
    result = requests.post(webhook_url, json = data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))
    
# run backend    
if __name__ == "__main__":
    app.run(host="localhost", port=5000)