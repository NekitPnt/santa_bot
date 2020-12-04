from flask import Flask, request
from peewee import SqliteDatabase
import traceback
import git

import utils
import settings
from classes import payloadClass, soClass, userClass
import comanager as cmng
from features import secret_santa

app = Flask(__name__)
database = SqliteDatabase(settings.DATABASE)


@app.before_request
def before_request():
    database.connect()


@app.after_request
def after_request(response):
    database.close()
    return response

# ---------------------------------------------------------------------------------------------------------------------
# Основные боты
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route('/git_hook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('./Santa_bot')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


# VK
@app.route('/vk', methods=['POST'])
def processing():
    data = request.get_json(force=True)
    if 'type' not in data:
        return 'not vk'
    else:
        if data['type'] == 'confirmation':
            return settings.vk_confirmation_token
        return response_handler_for_vk(data)


# ---------------------------------------------------------------------------------------------------------------------
# обработчики данных от вк и тг
# ---------------------------------------------------------------------------------------------------------------------
# -------------------------------------- обработчик входящих запросов от VK -------------------------------------------

def response_handler_for_vk(data):
    try:
        if (data['type'] == 'message_new' or data['type'] == 'message_edit') and \
                data['object']['from_id'] != -settings.vk_group_id and \
                data['object']['from_id'] == data['object']['peer_id']:
            data['object']['payload'] = payloadClass.get_payload(data['object'].get('payload', "{}"))
            # выковыривание рефералки
            if 'ref' in data['object']:
                data['object']['text'] = data['object']['ref']
            # выковыривание из пересланных кода join
            if data['object'].get('fwd_messages', ''):
                data['object']['text'] = utils.fwd_parser(data['object'])
            return create_answer(data['object'], soClass.vk_soc)
        elif data['type'] == 'message_event':
            payload: payloadClass.Payload = payloadClass.get_payload(data['object']['payload'])
            data['object']['payload'] = payload
            data['object']['text'] = payload.command
            data['object']['from_id'] = data['object']['user_id']
            return create_answer(data['object'], soClass.vk_soc)
        elif data['type'] == 'group_leave':
            pass
        elif data['type'] == 'group_join':
            pass
        """elif data['type'] == 'message_allow':
            utils.msg_allowed(data['object']['user_id'], soClass.vk_soc)  # todo
        elif data['type'] == 'message_deny':
            utils.msg_denied(data['object']['user_id'], soClass.vk_soc)  # todo"""
        return 'ok'
    except Exception:
        utils.error_notificator(traceback.format_exc() + '\n\n' + str(data))
        return 'ok'


# ---------------------------------------------------------------------------------------------------------------------
# генератор ответов
# ---------------------------------------------------------------------------------------------------------------------


def create_answer(data: dict, social: soClass.Socials) -> str:
    # инициализация юзерского объекта
    user = userClass.User(social, data)

    data['text'] = data.get('text', '')
    command: str = data['text'].lower().replace('/start ', '').strip()

    # -------------------------------------- основная функциональность ------------------------------------------------
    # только для админов
    if user.is_admin:
        # кик юзера
        if command.startswith(cmng.kick_user.prefix):
            secret_santa.kick_user_from_room(user, command)
        # начать шафлинг
        elif command in cmng.start_shuffle.activators or command in cmng.reshuffle.activators:
            secret_santa.start_gifts_shuffle(user)
        # проверка количества юзеров в комнате
        elif command in cmng.check_room.activators:
            secret_santa.check_users_in_room(user)
        # удаление комнаты
        elif command in cmng.delete_room.activators:
            secret_santa.clear_room(user)
    # инфа о том что умеет бот
    if command in cmng.about.activators:
        secret_santa.about_response(user)
    # создание новой комнаты
    elif command in cmng.room_creation.activators:
        secret_santa.create_room(user)
    # выход из комнаты
    elif command in cmng.user_leave.activators:
        secret_santa.user_leave_room(user)
    # заход по ссылке в комнату участника
    elif command.startswith(cmng.user_adding.prefix):
        secret_santa.add_user_to_room(user, command)

    # --------------------------------------------------------------------------------------

    return 'ok'


# ---------------------------------------------------------------------------------------------------------------------
# граб ошибок и отправка их в лс админу
# ---------------------------------------------------------------------------------------------------------------------


@app.errorhandler(500)
def error_handler(e):
    # уведомляете админа об ошибке
    utils.error_notificator(traceback.format_exc())
    # print(traceback.format_exc())
    # возвращаете ВК ok
    return 'ok'

# todo list
# прогуглить про партнерство с озоном через регистрации
# прогуглить про партнерские сервисы
# сделать анеки
# сделать фанты
#
