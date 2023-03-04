#!/usr/bin/env bash
# exit on error
set -o errexit

pip install requirements.txt

mv youtubesearchpython /usr/local/lib/python3.11/site-packages/

python manage.py collectstatic --no-input
python manage.py migrate