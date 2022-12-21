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
        # стейтовые фичи
        if (state := user.get_state()) is not None:
            # -------------------------- только для админов ---------------------------
            # кик юзера
            if state == features.kick_user.state_key and user.is_admin:
                secret_santa.kick_user_from_room(user, command)
            # удаление комнаты
            elif state == features.delete_room.state_key and user.is_admin:
                secret_santa.clear_room(user, command)
            # -------------------------- для обычных юзеров --------------------------
            # выход из комнаты
            elif state == features.user_leave.state_key:
                secret_santa.user_leave_room(user, command)
            # создание/перезапись вишлиста
            elif state == features.create_wish_list.state_key:
                secret_santa.process_create_wish_list(user, command)
            # дополнение вишлиста
            elif state == features.append_wish_list.state_key:
                secret_santa.process_append_wish_list(user, command)
            else:
                secret_santa.state_error(user)
        else:
            # -------------------------- только для админов ---------------------------
            # апрув кика юзера
            if command.startswith(features.kick_user.prefix) and user.is_admin:
                secret_santa.approve_kick_user_from_room(user, command)
            # начать шафлинг
            elif command in (features.start_shuffle.activators + features.reshuffle.activators) and user.is_admin:
                secret_santa.start_gifts_shuffle(user)
            # проверка количества юзеров в комнате
            elif command in features.check_room.activators and user.is_admin:
                secret_santa.check_users_in_room(user)
            # апрув удаления комнаты
            elif command in features.delete_room.activators and user.is_admin:
                secret_santa.approve_clear_room(user)
            # -------------------------- для обычных юзеров --------------------------
            # инфа о том что умеет бот
            elif command in features.about.activators:
                secret_santa.about_response(user)
            # правила игры в санту + help
            elif command in features.rules_and_help.activators:
                secret_santa.help_request(user)
            # создание новой комнаты
            elif command in features.room_creation.activators:
                secret_santa.create_room(user)
            # апрув выхода из комнаты
            elif command in features.user_leave.activators:
                secret_santa.approve_user_leave_room(user)
            # меню вишлиста
            elif command.startswith(features.wish_list_menu.prefix):
                secret_santa.wishlist_menu_response(user)
            # создание вишлиста
            elif command in features.create_wish_list.activators:
                secret_santa.wishlist_create_response(user)
            # дополнение вишлиста
            elif command in features.append_wish_list.activators:
                secret_santa.wishlist_append_response(user)
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
