#!/bin/bash -e
PATH=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin
eval "$(ssh-agent -s)"
ssh-add /home/santabot/.ssh/santa_bot_dk
cd /home/santabot/santa_bot
git pull
docker-compose build && docker-compose stop && docker-compose up -d --force-recreate