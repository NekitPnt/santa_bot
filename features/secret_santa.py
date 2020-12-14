from classes.userClass import User
from classes.msgCls import Message
from classes.btnCls import Btn
from classes import myVkbotClass, msend
import comanager as cmng
from lib import join_link_creator
import settings
from models import Users

import random

vk_methods = myVkbotClass.VkMethods(settings.vk_token, settings.vk_api_version)


def about_response(user: User):
    # если у чувака уже есть комната
    if user.room_id:
        # если он админ этой комнаты тогда предлагаем ему кикнуть, узнать список людей, зашафлить
        if user.is_admin:
            msg = Message(f"{cmng.admin_about.text}\n", [])
            # если комната уже создана, напоминаем ключ захода в нее
            if user.room_id:
                key, vk_link = join_link_creator.create_join_link_and_key(cmng.user_adding.prefix, user.room_id)
                user.send_msg(Message(f"Напоминаю код комнаты: {key}\nИ ссылку: {vk_link}"))
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
    if not vk_methods.check_user_sub(settings.vk_group_id, user.uid):
        user.send_msg(Message(cmng.pls_sub.text))
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
        if room == 'exists':
            msg = Message('Вы уже в комнате, вам не нужно переходить по ссылке или скидывать мне код')
        elif room:
            # пишем юзеру в чью комнату он зашел
            room_admin_id = Users.get(social=user.social.key, room_id=room_id, is_admin=True).user_social_id
            room_admin_name = vk_methods.linked_user_name(room_admin_id)
            msg = Message(cmng.user_adding.text.format(room_admin_name))
            # пишем админу что в его комнату зашли
            user_name = vk_methods.linked_user_name(user.uid)
            msend.send_msg(room_admin_id, user.social, Message(cmng.user_adding.descr.format(user_name)))
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
        getter = User(admin.social, uid=getter_id)
        getter_wishlist = getter.get_wishlist()
        text = f"{getter_link} {cmng.start_shuffle.text}. Кстати, его(ее) вишлист: {getter_wishlist}" \
            if getter_wishlist else f"{getter_link} {cmng.start_shuffle.text}"
        msg = Message(text)
        msend.send_msg(sender_id, admin.social, msg)
        msend.send_msg(sender_id, admin.social, Message(cmng.pls_sub.text))

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
    user = User(admin.social, uid=user_id)
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
        msg = Message(cmng.wish_list_error.text)
    else:
        # save wishlist
        user.save_wishlist(wishlist)
        msg = Message(cmng.wish_list.text.format(wishlist))
    user.send_msg(msg)
