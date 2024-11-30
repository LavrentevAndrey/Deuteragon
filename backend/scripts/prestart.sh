#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python app/db_main.py

# Create initial data in DB
python app/initial_data.py
