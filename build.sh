#!/usr/bin/env bash
# Render build script
# Build Command: ./build.sh
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py compilemessages -l en
python manage.py createsuperuser --noinput || true