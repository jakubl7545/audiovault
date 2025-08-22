#!/bin/bash
flask db upgrade
exec gunicorn -c gunicorn_config.py app:app
