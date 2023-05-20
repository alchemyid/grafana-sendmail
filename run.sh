#!/bin/bash
gunicorn --reload --chdir /opt -w 3 --threads 3 -b 0.0.0.0:8000 --timeout 300 --access-logfile '-' 'app:http()'