#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

mv youtubesearchpython /venv/lib/site-packages/

python manage.py collectstatic --no-input
python manage.py migrate