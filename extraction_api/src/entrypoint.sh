#!/bin/bash
set -e

CWD=$(cd $(dirname $0); pwd)

# TODO: is event broker up and running?

# run Flask API
exec uwsgi --chdir $CWD --wsgi-file main.py --callable app "$@"
