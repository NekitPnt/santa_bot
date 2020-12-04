from classes.userClass import User
from classes.msgCls import Message
from classes.btnCls import Btn
from classes import myVkbotClass
import comanager as cmng
from lib import join_link_creator
import settings

import random

vk_methods = myVkbotClass.VkMethods(settings.vk_token[settings.prod], settings.vk_api_version)


def about_response(user: User):
    # если у чувака уже есть комната
    if user.room_id:
        # если он админ этой комнаты тогда предлагаем ему кикнуть, узнать список людей, зашафлить
        if user.is_admin:
            msg = Message(f"{cmng.admin_about.text}\n", [])
            for ftr in [cmng.check_room, cmng.start_shuffle, cmng.delete_room]:
                if ftr is cmng.start_shuffle and user.get_room_shuffled():
                    ftr = cmng.reshuffle
                msg.text += f"\n — {ftr.descr};"
                msg.kb.append([Btn(ftr.button, color=ftr.button_color)])
        # иначе сообщаем юзеру что он сейчас в комнате и предлагаем только ливнуть оттуда
        else:
            msg = Message(f"{cmng.user_about.text}\n", [])
            msg.text += f"\n — {cmng.user_leave.descr};"
            msg.kb.append([Btn(cmng.user_leave.button)])
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
    key, vk_link = join_link_creator.create_join_link_and_key(cmng.user_adding.prefix, room_id)
    msg = Message(f"{cmng.room_creation.text}\n\nКод: {key}\nСсылка: {vk_link}")
    user.send_msg(msg)
    about_response(user)


def clear_room(admin: User):
    all_room_users = admin.clear_room()
    for user_social_id in all_room_users:
        user = User(admin.social, uid=user_social_id)
        user.send_msg(Message(cmng.delete_room.text))
    about_response(admin)


def add_user_to_room(user: User, command: str):
    room_id = join_link_creator.parse_key(command, cmng.user_adding.prefix)
    if room_id:
        room = user.set_room(room_id)
        msg = Message(cmng.user_adding.text) if room else Message(cmng.room_error.text)
    else:
        msg = Message(cmng.room_error.text)
    user.send_msg(msg)
    about_response(user)


def user_leave_room(user: User):
    user.leave_room()
    msg = Message(cmng.user_leave.text, [[Btn(cmng.room_creation.button)]])
    user.send_msg(msg)


def start_gifts_shuffle(admin: User):
    members = [i.user_social_id for i in admin.get_all_room_users()]
    random.shuffle(members)
    members.append(members[0])

    for uid_i in range(len(members) - 1):
        sender_id = members[uid_i]
        getter_id = members[uid_i + 1]
        sender = User(admin.social, uid=sender_id)
        getter_link = vk_methods.linked_user_name(getter_id)
        msg = Message(f"{getter_link} {cmng.start_shuffle.text}")
        sender.send_msg(msg)

    msg = Message(cmng.sucseed_shuffle.text, [[Btn(cmng.about.button)]])
    admin.room_shuffled()

    admin.send_msg(msg)


def check_users_in_room(admin: User):
    all_users = list(admin.get_all_room_users())
    admin.send_msg(Message(cmng.check_room.text))
    for user in all_users:
        user_name = vk_methods.linked_user_name(user.user_social_id)
        kb = [[Btn(f"{cmng.kick_user.button} {user.user_social_id}")]]
        admin.send_msg(Message(user_name, kb, inline_kb=True))
    about_response(admin)


def kick_user_from_room(admin: User, command: str):
    user_id = command.replace(cmng.kick_user.button.lower(), '').strip()
    user = User(admin.social, uid=user_id)
    user_name = vk_methods.linked_user_name(user_id)
    admin.send_msg(Message(cmng.kick_user.text.format(user_name)))
    admin.kick_user(user.db_id)
    user.send_msg(Message(cmng.kicked_user.text))
