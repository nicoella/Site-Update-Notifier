import time

from pymongo.mongo_client import MongoClient
from pymongo import MongoClient

from site_update_notifier.config import config # Place your Mongo URI in a config.py file
from site_update_notifier.utils import get_site_hash, send_notification

mongo_client = MongoClient(config["MONGO_URI"])

db = mongo_client["Cluster0"] # Update with your Cluster name

collection = db["data"] # Update with your Collection name

# check if site was updated    
def check_update(_id, url, hash, webhook):
    cur_hash = get_site_hash(url)
    if cur_hash != hash:
        send_notification(webhook, "Site Updated", "Your saved site " + url + " has had updates.")
        new_data = { "url": url, "hash": cur_hash, "webhook": webhook }
        update_result = collection.update_one({"_id": _id}, {"$set": new_data}).acknowledged
        print(update_result)

        
# get all data from backend
def get_all_data():
    data = collection.find()
    for site in data:
        check_update(site['_id'], site['site'], site['hash'], site['webhook'])
    
# check updates
def run_updates():
    run_count = 0
    while True:
        run_count += 1
        print("Checking for updates: #" + str(run_count))
        get_all_data()
        time.sleep(30)