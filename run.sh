#!/bin/bash

# Start venv
source venv/bin/activate

# Run backend
python manage.py runserver

# Run frontend
cd frontend
npm run start