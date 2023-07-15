from pymongo.mongo_client import MongoClient
from pymongo import MongoClient

from site_update_notifier.config import config # Place your Mongo URI in a config.py file

from django.urls import path
from django.http import HttpResponse, JsonResponse

from site_update_notifier.utils import get_site_hash, hash_str, send_notification

mongo_client = MongoClient(config["MONGO_URI"])

db = mongo_client["Cluster0"] # Update with your Cluster name

collection = db["data"] # Update with your Collection name

# base for api
def welcome(request):
    return HttpResponse("api is running")

# update database POST request
def insert_data(request):
    if request.method == "POST":
        data = request.POST
        site = data.get("site")
        webhook = data.get("webhook")
        hash_value = get_site_hash(site)
        hash_id = hash_str(site+" "+webhook)
        try:
            insert_result = collection.insert_one({"_id": hash_id, "site":site, "hash":hash_value, "webhook":webhook}).acknowledged
            if not insert_result:
                return JsonResponse({"status": "bad insert"})
            if not send_notification(webhook, "Webhook Added", f"Your webhook has been added for the site {site}. Update notifications will be sent here."):
                collection.delete_one({"_id": hash_id})
                return JsonResponse({"status": "bad webhook"})
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method"})

# check database status
def ping_mongodb(request):
    try:
        mongo_client.admin.command('ping')
        return HttpResponse("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        return HttpResponse(str(e))