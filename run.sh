#!/bin/bash
export PATH="$PATH:/opt/.local/bin"
gunicorn --reload --chdir /opt -w 1 --threads 1 -b 0.0.0.0:8000 --timeout 300 --access-logfile '-' 'app:http()'