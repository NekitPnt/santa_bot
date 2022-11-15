import random
import time
from typing import Tuple

from santa_vk_bot.classes.userClass import User
from santa_vk_bot.classes.msgCls import Message, Btn
from santa_vk_bot.classes import myVkbotClass
from santa_vk_bot import features as cmng, msg_send
from santa_vk_bot.config import settings
from santa_vk_bot.models import Users

vk_methods = myVkbotClass.VkMethods(settings.vk_bot_token, settings.vk_api_version)


def create_join_link_and_key(join_prefix: str, room_id: int) -> Tuple[str, str]:
    key = f"{join_prefix}{int(time.time())}{room_id}{len(str(room_id))}"
    vk_link = f'vk.me/-{settings.vk_group_id}?ref={key}'
    return key, vk_link


def parse_key(command: str, join_prefix) -> int:
    ref_code = command.replace(join_prefix, '').strip()
    if not ref_code:
        return 0
    num_len = int(ref_code[-1]) if ref_code[-1].isdigit() else 0
    if not num_len:
        return num_len
    return int(ref_code[-num_len-1:-1]) if ref_code[-num_len-1:-1].isdigit() else 0


def about_response(user: User):
    # если у чувака уже есть комната
    if user.room_id:
        # если он админ этой комнаты тогда предлагаем ему кикнуть, узнать список людей, зашафлить
        if user.is_admin:
            msg = Message(f"{cmng.admin_about.text}\n", [])
            # если комната уже создана, напоминаем ключ захода в нее
            if user.room_id:
                key, vk_link = create_join_link_and_key(cmng.user_adding.prefix, user.room_id)
                user.send_msg(Message(f"Напоминаю код комнаты: {key}\nИ ссылку: {vk_link}"))
            for ftr in [cmng.wish_list, cmng.check_room, cmng.start_shuffle, cmng.delete_room]:
                if ftr is cmng.start_shuffle and user.get_room_shuffled():
                    ftr = cmng.reshuffle
                msg.text += f"\n — {ftr.descr};"
                msg.kb.append([Btn(ftr.button, color=ftr.button_color)])
        # иначе сообщаем юзеру что он сейчас в комнате и предлагаем ливнуть оттуда или запилить вишлист
        else:
            msg = Message(f"{cmng.user_about.text}\n", [])
            for ftr in [cmng.wish_list, cmng.user_leave]:
                msg.text += f"\n — {ftr.descr};"
                msg.kb.append([Btn(ftr.button, color=ftr.button_color)])
    # предлагаем создать комнату
    else:
        msg = Message(f"{cmng.about.text}\n", [])
        msg.text += f"\n — {cmng.room_creation.descr};"
        msg.kb.append([Btn(cmng.room_creation.button)])

    user.send_msg(msg)


def create_room(user: User):
    # создаем новую комнату, назначаем юзера админом, возвращаем ему ключ захода и ссылку
    room_id = user.create_room()
    # генерируем ключ для захода
    key, vk_link = create_join_link_and_key(cmng.user_adding.prefix, room_id)
    msg = Message(f"{cmng.room_creation.text}\n\nКод: {key}\nСсылка: {vk_link}")
    user.send_msg(msg)
    if not vk_methods.check_user_sub(settings.vk_group_id, user.uid):
        user.send_msg(Message(cmng.pls_sub.text))
    about_response(user)


def clear_room(admin: User):
    all_room_users = admin.clear_room()
    for user_social_id in all_room_users:
        user = User(uid=user_social_id)
        user.send_msg(Message(cmng.delete_room.text))
    about_response(admin)


def add_user_to_room(user: User, command: str):
    room_id = parse_key(command, cmng.user_adding.prefix)
    if room_id:
        room = user.set_room(room_id)
        if room == 'exists':
            msg = Message('Вы уже в комнате, вам не нужно переходить по ссылке или скидывать мне код')
        elif room:
            # пишем юзеру в чью комнату он зашел
            room_admin_id = Users.get_or_none(room_id=room_id, is_admin=True)
            if room_admin_id:
                room_admin_name = vk_methods.linked_user_name(room_admin_id.user_social_id)
                msg = Message(cmng.user_adding.text.format(room_admin_name))
                # пишем админу что в его комнату зашли
                user_name = vk_methods.linked_user_name(user.uid)
                msg_send.send_msg(user_id=room_admin_id.user_social_id,
                                  msg=Message(cmng.user_adding.descr.format(user_name)))
            else:
                msg = Message(cmng.user_adding.text.format(''))
        else:
            msg = Message(cmng.room_error.text)
    else:
        msg = Message(cmng.room_error.text)
    user.send_msg(msg)
    about_response(user)


def user_leave_room(user: User):
    user.leave_room()
    msg = Message(cmng.user_leave.text, [[Btn(cmng.room_creation.button)]])
    user.send_msg(msg)


def start_gifts_shuffle(admin: User):
    # закольцовываем список участников
    members = [i.user_social_id for i in admin.get_all_room_users()]
    random.shuffle(members)
    members.append(members[0])

    for uid_i in range(len(members) - 1):
        sender_id = members[uid_i]
        getter_id = members[uid_i + 1]
        getter_link = vk_methods.linked_user_name(getter_id)
        # подгружаем вишлист
        getter = User(uid=getter_id)
        getter_wishlist = getter.get_wishlist()
        text = f"{getter_link} {cmng.start_shuffle.text}. Кстати, его(ее) вишлист: {getter_wishlist}" \
            if getter_wishlist else f"{getter_link} {cmng.start_shuffle.text}"
        msg = Message(text)
        msg_send.send_msg(user_id=sender_id, msg=msg)
        msg_send.send_msg(user_id=sender_id, msg=Message(cmng.pls_sub.text))

    admin.room_shuffled()


def check_users_in_room(admin: User):
    all_users = list(admin.get_all_room_users())
    admin.send_msg(Message(cmng.check_room.text))
    for user in all_users:
        user_name = vk_methods.linked_user_name(user.user_social_id)
        kb = [[Btn(f"{cmng.kick_user.button} {user.user_social_id}")]]
        admin.send_msg(Message(user_name, kb, inline_kb=True))
    about_response(admin)


def kick_user_from_room(admin: User, command: str):
    # парсим юзера из его социальной айди
    user_id = command.replace(cmng.kick_user.button.lower(), '').strip()
    user = User(uid=user_id)
    user_name = vk_methods.linked_user_name(user_id)
    # кикаем
    admin.kick_user(user.db_id)
    # говорим и админу и юзеру о кике
    admin.send_msg(Message(cmng.kick_user.text.format(user_name)))
    user.send_msg(Message(cmng.kicked_user.text))
    about_response(admin)


def wrong_request(user: User):
    my_name = vk_methods.linked_user_name(settings.error_receiver_id)
    user.send_msg(Message(cmng.wrong_command.text.format(my_name)))
    about_response(user)


def save_wishlist(user: User, command: str):
    # validate wishlist
    wishlist = command.replace(cmng.wish_list.prefix, '').strip()
    if not wishlist:
        # если у юзера уже есть вишлист, показываем его ему
        user_wl = user.get_wishlist()
        if user_wl:
            msg = Message(cmng.wish_list_error.descr.format(user_wl, cmng.wish_list_creation))
        # если нет, говорим об ошибке
        else:
            msg = Message(cmng.wish_list_error.text)
    else:
        # save wishlist
        user.save_wishlist(wishlist)
        msg = Message(cmng.wish_list.text.format(wishlist))
    msg.kb = [[Btn(cmng.about.button)]]
    user.send_msg(msg)
