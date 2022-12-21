# Santa_bot
VK чат-бот для игры в тайного санту, подробности в группе: https://vk.com/mysterysanta

## Changelogs
### v2.1 changelog
1) добавлены подтверждения для критических действий: удаление комнаты, кик участника, выход из комнаты
2) при выходе из комнаты об этом уведомляется админ
3) перед шафлом бот рассылает проверочные сообщения чтобы убедиться что все готовы. Если кто-то заблокировал бота, вместо шафла бот уведомит об этом админа комнаты
4) результаты шафла записываются в бд
5) новая команда /help в которой описаны основные правила игры в тайного и санта и гайд как пользоваться ботом
6) вишлист теперь в отдельном меню, убрана механика префикса. Теперь его можно создавать(перезаписывать) и дополнять
7) лайв обновление вишлиста: теперь его можно обновлять и после шафла. При обновлении вишлиста бот отошлет свежую версию тому, кто вам дарит подарок
8) фикс мелких багов

### v2.0 changelog
перевод бота с callback на longpoll, докеризация, замена БД на постгрес

## Project Setup
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
4. git clone <ssh string> на сервере в папку юзера
5. установка docker, docker-compose
6. в консоли ```sudo chown $USER /var/run/docker.sock```
7. в папке проекта (cd santa_bot) прописываем переменные окружения в .env файл (образец в файле template.env)
8. сделать скрипты выполняемыми ```chmod +x santa_bot/santa_bot_deploy.sh``` и ```chmod +x santa_bot/santa_bot_reload.sh```

### Деплой:
- пуш в гит
- на сервере команда ```./santa_bot/santa_bot_deploy.sh```.

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
