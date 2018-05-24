#!/bin/sh
source .venv/bin/activate
celery worker -A neam.python.app.celery -E --loglevel=info

