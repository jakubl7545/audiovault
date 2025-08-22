#!/bin/bash
flask db upgrade
exec gunicorn -b :5000 -k gevent --access-logfile - --error-logfile - app:app
