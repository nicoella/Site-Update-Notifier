#!/bin/bash

# Activate venv
python3 -m venv venv

# Start venv
source venv/bin/activate

# Install dependencies
pip install beautifulsoup4 requests
python -m pip install pymongo==3.11

# Install node modules
cd frontend
npm install