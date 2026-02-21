#!/bin/bash
set -ex 

# Collect static files
python manage.py collectstatic --no-input
# Launch the application
gunicorn gamer_journey.wsgi:application --bind 0.0.0.0:$PORT
