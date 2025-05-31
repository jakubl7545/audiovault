#!/bin/bash
flask db upgrade
exec gunicorn -b :5000 -t 0 --access-logfile - --error-logfile - app:app
