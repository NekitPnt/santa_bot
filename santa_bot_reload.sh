#!/bin/bash -e
PATH=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin
cd /home/santabot/santa_bot
docker-compose stop && docker-compose up -d --force-recreate