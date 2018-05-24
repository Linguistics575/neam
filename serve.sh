#!/bin/sh
source .venv/bin/activate
export FLASK_APP=$PWD/serve.py
# export PYWIKIBOT2_NO_USER_CONFIG=1
flask run
