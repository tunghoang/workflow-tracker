SERVER_NAME=pptracker.duckdns.org:8000 /home/apom/pipeline-tracker/.appenv/bin/gunicorn -c gconfig.py --pythonpath /home/apom/pipeline-tracker/.appenv/bin app:app
