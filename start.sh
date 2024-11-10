#!/bin/sh

crontab /root/cron.txt

python3 /root/server.py &
crond -f
