#!/bin/bash
# Install dependencies
pip3 install -r requirements.txt

# Collect static files
python3.9 manage.py collectstatic --noinput