from flask import Flask, request
from peewee import SqliteDatabase
import traceback
import telebot
import git

import utils
import settings
from classes import payloadClass, soClass, userClass
import comanager as cmng
from features import secret_santa

app = Flask(__name__)
tg_bot = telebot.TeleBot(settings.tg_token[settings.prod])
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


# Telegram
@app.route("/telegram", methods=['POST'])
def tp_tg_webhook():
    data = request.get_json(force=True)
    if 'message' in data:
        return response_handler_for_tg(data['message'])
    elif 'callback_query' in data:
        return callback_query_handler(data)
    else:
        return 'not tg'


@app.route('/git_hook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('./Santa_bot')
        origin = repo.remotes.origin
        repo.create_head('master',
                         origin.refs.master).set_tracking_branch(origin.refs.master).checkout()
        origin.pull()
        return '', 200
    else:
        return '', 400


# VK
@app.route('/vk', methods=['POST'])
def processing():
    data = request.get_json(force=True)
    if 'type' not in data:
        return 'not vk'
    else:
        if data['type'] == 'confirmation':
            return settings.vk_confirmation_token[settings.prod]
        return response_handler_for_vk(data)


# ---------------------------------------------------------------------------------------------------------------------
# обработчики данных от вк и тг
# ---------------------------------------------------------------------------------------------------------------------
# -------------------------------------- обработчик входящих запросов от VK -------------------------------------------

def response_handler_for_vk(data):
    try:
        if (data['type'] == 'message_new' or data['type'] == 'message_edit') and \
                data['object']['from_id'] != -settings.vk_group_id[settings.prod] and \
                data['object']['from_id'] == data['object']['peer_id']:
            data['object']['payload'] = payloadClass.get_payload(data['object'].get('payload', "{}"))
            if 'ref' in data['object']:
                data['object']['text'] = data['object']['ref']
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


# -------------------------------------- обработчик входящих запросов от TG -------------------------------------------


def response_handler_for_tg(data):
    try:
        return create_answer(data, soClass.tg_soc)
    except Exception:
        utils.error_notificator(traceback.format_exc() + '\n\n' + str(data))
        return 'ok'


def answer_callback_tg(callback_query_id, text='', show_alert=False):
    tg_bot.answer_callback_query(callback_query_id, text, show_alert)


# обработчик запросов инлайновых кнопок
def callback_query_handler(data):
    new_data = data['callback_query']['message']
    new_data['message_text'] = new_data['text']
    new_data['callback_query_id'] = data['callback_query']['id']
    callback_data = data['callback_query']['data']
    payload: payloadClass.Payload = payloadClass.get_payload(callback_data)
    new_data['payload'] = payload
    new_data['text'] = payload.command

    if not payload.answ_back:
        answer_callback_tg(data['callback_query']['id'])

    return response_handler_for_tg(new_data)

# ---------------------------------------------------------------------------------------------------------------------
# генератор ответов
# ---------------------------------------------------------------------------------------------------------------------


def create_answer(data: dict, social: soClass.Socials) -> str:
    # инициализация юзерского объекта
    user = userClass.User(social, data)

    data['text'] = data.get('text', '')
    command: str = data['text'].lower().replace('/start ', '').strip()

    # -------------------------------------- основная функциональность ------------------------------------------------
    # инфа о том что умеет бот
    if command in cmng.about.activators:
        secret_santa.about_response(user)
    # создание новой комнаты
    elif command in cmng.room_creation.activators:
        secret_santa.create_room(user)
    # выход из комнаты
    elif command in cmng.user_leave.activators:
        secret_santa.user_leave_room(user)
    # кик юзера
    elif command.startswith(cmng.kick_user.prefix):
        secret_santa.kick_user_from_room(user, command)
    # начать шафлинг
    elif command in cmng.start_shuffle.activators or command in cmng.reshuffle.activators:
        secret_santa.start_gifts_shuffle(user)
    # проверка количества юзеров в комнате
    elif command in cmng.check_room.activators:
        secret_santa.check_users_in_room(user)
    # проверка количества юзеров в комнате
    elif command in cmng.delete_room.activators:
        secret_santa.clear_room(user)
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
    # возвращаете ВК ok
    return 'ok'
