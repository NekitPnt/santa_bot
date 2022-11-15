import traceback
import threading

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll

from santa_vk_bot import features
from santa_vk_bot.classes import payloadClass, userClass, msgCls
from santa_vk_bot.config import settings
from santa_vk_bot.handlers import secret_santa


def fwd_parser(data: dict):
    for mes in data.get('fwd_messages', []):
        if mes.get('fwd_messages', ''):
            return fwd_parser(mes)
        else:
            if features.user_adding.prefix in mes.get('text', ''):
                splitted_mes = mes.get('text', '').split()
                for i in splitted_mes:
                    if i.startswith(features.user_adding.prefix):
                        return i
    return ''


def error_notificator(error: any):
    error = str(error)
    print(error)
    try:
        admin = userClass.User(uid=settings.error_receiver_id)
        admin.send_msg(msgCls.Message(error))
    except Exception as e:
        print(f'Error in error_notificator: {e}')


error_notificator('reload succeed')


# ---------------------------------------------------------------------------------------------------------------------
# генератор ответов
# ---------------------------------------------------------------------------------------------------------------------
def create_answer(data: dict):
    try:
        # инициализация юзерского объекта
        user = userClass.User(data=data)

        data['text'] = data.get('text', '')
        command: str = data['text'].lower().replace('/start ', '').strip()

        # -------------------------------------- основная функциональность --------------------------------------------
        # только для админов
        # кик юзера
        if command.startswith(features.kick_user.prefix) and user.is_admin:
            secret_santa.kick_user_from_room(user, command)
        # начать шафлинг
        elif (command in (features.start_shuffle.activators + features.reshuffle.activators)) and user.is_admin:
            secret_santa.start_gifts_shuffle(user)
        # проверка количества юзеров в комнате
        elif command in features.check_room.activators and user.is_admin:
            secret_santa.check_users_in_room(user)
        # удаление комнаты
        elif command in features.delete_room.activators and user.is_admin:
            secret_santa.clear_room(user)
        # инфа о том что умеет бот
        elif command in features.about.activators:
            secret_santa.about_response(user)
        # создание новой комнаты
        elif command in features.room_creation.activators:
            secret_santa.create_room(user)
        # выход из комнаты
        elif command in features.user_leave.activators:
            secret_santa.user_leave_room(user)
        # вишлист
        elif command.startswith(features.wish_list.prefix):
            secret_santa.save_wishlist(user, command)
        # заход по ссылке в комнату участника
        elif command.startswith(features.user_adding.prefix):
            secret_santa.add_user_to_room(user, command)
        else:
            secret_santa.wrong_request(user)
    except Exception:
        error_notificator(traceback.format_exc() + '\n\n' + str(data))


# ---------------------------------------------------------------------------------------------------------------------
# пулинг бота
# ---------------------------------------------------------------------------------------------------------------------


def main():
    vk_session = vk_api.VkApi(token=settings.vk_bot_token)
    longpoll = VkBotLongPoll(vk_session, settings.vk_group_id)
    for event in longpoll.listen():
        data = event.raw
        if (data['type'] == 'message_new' or data['type'] == 'message_edit') and \
                data['object']['from_id'] != -settings.vk_group_id and \
                data['object']['from_id'] == data['object']['peer_id']:
            data['object']['payload'] = payloadClass.get_payload(data['object'].get('payload', "{}"))
            # выковыривание рефералки
            if 'ref' in data['object']:
                data['object']['text'] = data['object']['ref']
            # выковыривание из пересланных кода join
            if data['object'].get('fwd_messages', ''):
                data['object']['text'] = fwd_parser(data['object'])
            threading.Thread(target=create_answer, args=[data['object']]).start()
        elif data['type'] == 'message_event':
            payload: payloadClass.Payload = payloadClass.get_payload(data['object']['payload'])
            data['object']['payload'] = payload
            data['object']['text'] = payload.command
            data['object']['from_id'] = data['object']['user_id']
            threading.Thread(target=create_answer, args=[data['object']]).start()


if __name__ == '__main__':
    main()
