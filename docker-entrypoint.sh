#!/bin/sh
set -e
flask db upgrade
python app.py