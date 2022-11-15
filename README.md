# Santa_bot
This is chat bot for Vk, created for playing secret santa

### Предварительная настройка:
1. пуш в мастер самые последние изменения в ветке
2. [настройка гита на сервере](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key)
   1. если на сервере нужно сделать деплой нескольких репозиториев, то файл ```nano ~/.ssh/config```:
   ```
   Host github.com-<repo name>
     AddKeysToAgent yes
     Hostname github.com
     IdentityFile=/home/<user>/.ssh/<dk key>```
3. [настройка деплой ключа в репо](https://docs.github.com/en/developers/overview/managing-deploy-keys#deploy-keys)
4. клон репо на сервер
5. установка docker, docker-compose
6. в папке проекта (cd santa_vk_bot) прописываем переменные окружения в .env файл (образец в файле template.env)
7. скрипты ```santa_bot_reload.sh``` и ```santa_bot_deploy.sh``` необходимо вынести на папку выше проекта

### Деплой:
- пуш в гит
- на сервере команда ```./santa_bot_deploy.sh```. Скрипт необходимо вынести на папку выше проекта

### Как подключиться к базе из менеджера баз данных
- docker ps
- docker exec -ti <CONTAINER ID> /bin/sh
- psql -h ```<.env/POSTGRES_HOST>``` -p 5431 -U ```<.env/POSTGRES_USER>```
  - ```psql -h db -p 5432 -U db_user -d db``` для подключения внутри контейнера
- В ответ будет вывод ```psql: error: could not connect to server: Connection refused
        Is the server running on host "<.env/POSTGRES_HOST>" <IP ADDRESS> and accepting
        TCP/IP connections on port 5431?```
- Адрес хоста внутри контейнера будет ```<IP ADDRESS>```. При подключении надо использовать 5432 порт

### Переезд на другой сервер
1. Настроить докер
2. [Перенести базу](https://simplebackups.com/blog/docker-postgres-backup-restore-guide-with-examples/)
