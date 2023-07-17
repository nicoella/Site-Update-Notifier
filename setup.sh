#!/bin/bash

# Activate venv
python3 -m venv venv

# Start venv
source venv/bin/activate

# Install dependencies
pip install beautifulsoup4 requests
python -m pip install pymongo==3.11
pip install dnspython
pip install django

# Install node modules
cd frontend
npm install
cd ..

# Create config.py file
cd site_update_notifier
touch config.py
echo 'config = {
    "MONGO_URI":"[your_mongo_URI]",
    "MONGO_CLUSTER":"[your_mongo_cluster_name]", 
    "MONGO_COLLECTION":"[your_mongo_collection_name]",
}' > config.py