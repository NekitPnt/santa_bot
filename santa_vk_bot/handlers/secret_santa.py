import random
import time
from typing import Tuple

from santa_vk_bot.classes.userClass import User
from santa_vk_bot.classes.msgCls import Message, Btn
from santa_vk_bot.classes import myVkbotClass
from santa_vk_bot import features, msg_send
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
            msg = Message(f"{features.admin_about.text}\n", [])
            # если комната уже создана, напоминаем ключ захода в нее
            if user.room_id:
                key, vk_link = create_join_link_and_key(features.user_adding.prefix, user.room_id)
                user.send_msg(Message(f"Напоминаю код комнаты: {key}\nИ ссылку: {vk_link}"))
            for ftr in [features.wish_list_menu, features.check_room, features.start_shuffle, features.delete_room]:
                if ftr is features.start_shuffle and user.get_room_shuffled():
                    ftr = features.reshuffle
                msg.text += f"\n — {ftr.descr};"
                msg.kb.append([Btn(ftr.button, color=ftr.button_color)])
        # иначе сообщаем юзеру что он сейчас в комнате и предлагаем ливнуть оттуда или запилить вишлист
        else:
            admin = user.get_room_admin()
            admin_name = vk_methods.linked_user_name(admin.user_social_id) if admin else ""
            msg = Message(f"{features.user_about.text.format(admin_name=admin_name)}\n", [])
            for ftr in [features.wish_list_menu, features.user_leave]:
                msg.text += f"\n — {ftr.descr};"
                msg.kb.append([Btn(ftr.button, color=ftr.button_color)])
    # предлагаем создать комнату
    else:
        msg = Message(f"{features.about.text}\n", [])
        msg.text += f"\n — {features.room_creation.descr};"
        msg.kb.append([Btn(features.room_creation.button)])

    user.send_msg(msg)


def create_room(user: User):
    # создаем новую комнату, назначаем юзера админом, возвращаем ему ключ захода и ссылку
    room_id = user.create_room()
    # генерируем ключ для захода
    key, vk_link = create_join_link_and_key(features.user_adding.prefix, room_id)
    msg = Message(f"{features.room_creation.text}\n\nКод: {key}\nСсылка: {vk_link}")
    user.send_msg(msg)
    if not vk_methods.check_user_sub(settings.vk_group_id, user.uid):
        user.send_msg(Message(features.pls_sub.text))
    about_response(user)


def add_user_to_room(user: User, command: str):
    room_id = parse_key(command, features.user_adding.prefix)
    if room_id:
        room = user.set_room(room_id)
        if room == 'exists':
            msg = Message(features.room_error.text2)
        elif room:
            # пишем юзеру в чью комнату он зашел
            room_admin_id = Users.get_or_none(room_id=room_id, is_admin=True)
            if room_admin_id:
                room_admin_name = vk_methods.linked_user_name(room_admin_id.user_social_id)
                msg = Message(features.user_adding.text.format(room_admin_name))
                # пишем админу что в его комнату зашли
                user_name = vk_methods.linked_user_name(user.uid)
                admin_msg = Message(features.user_adding.descr.format(user_name), kb=[[Btn(features.about.button)]])
                msg_send.send_msg(user_id=room_admin_id.user_social_id, msg=admin_msg)
            else:
                msg = Message(features.user_adding.text.format(''))
        else:
            msg = Message(features.room_error.text)
    else:
        msg = Message(features.room_error.text)
    user.send_msg(msg)
    about_response(user)


def approve_kick_user_from_room(admin: User, command: str):
    # парсим юзера из его социальной айди
    try:
        user_id = command.replace(features.kick_user.button.lower(), '').strip()
        user = User(uid=user_id)
        user_name = vk_methods.linked_user_name(user_id)
        admin.set_state(state_key=features.kick_user.state_key)
        admin.send_msg(Message(features.kick_user.text2.format(user_name),
                               kb=[[Btn(f"{features.kick_user.button} {user.uid}")], [Btn(features.no_state.button)]]))
    except Exception:
        admin.send_msg(Message(features.kick_user_not_found.text,
                               kb=[[Btn(features.check_room.button)], [Btn(features.about.button)]]))


def kick_user_from_room(admin: User, command: str):
    # если админ передумал
    if command in features.no_state.activators:
        admin.send_msg(Message(features.no_state.text))
    else:
        try:
            # парсим юзера из его социальной айди
            user_id = command.replace(features.kick_user.button.lower(), '').strip()
            user_name = vk_methods.linked_user_name(user_id)
            # кикаем
            user = User(uid=user_id)
            admin.kick_user(user.db_id)
            # говорим и админу и юзеру о кике
            admin.send_msg(Message(features.kick_user.text.format(user_name)))
            admin_name = vk_methods.linked_user_name(admin.uid)
            user.send_msg(Message(features.kicked_user.text.format(admin_name=admin_name)))
        except Exception:
            admin.send_msg(Message(features.kick_user_not_found.text,
                                   kb=[[Btn(features.check_room.button)], [Btn(features.about.button)]]))
    admin.drop_state()
    about_response(admin)


def approve_clear_room(admin: User):
    admin.set_state(state_key=features.delete_room.state_key)
    admin.send_msg(Message(features.delete_room.text2,
                           kb=[[Btn(features.delete_room.button, color=features.delete_room.button_color)],
                               [Btn(features.no_state.button)]]))


def clear_room(admin: User, command: str):
    # если админ передумал
    if command in features.no_state.activators:
        admin.send_msg(Message(features.no_state.text))
    else:
        all_room_users = admin.clear_room()
        for user_social_id in all_room_users:
            user = User(uid=user_social_id)
            user.send_msg(Message(features.delete_room.text))
    admin.drop_state()
    about_response(admin)


def approve_user_leave_room(user: User):
    user.set_state(state_key=features.user_leave.state_key)
    user.send_msg(Message(features.user_leave_approve.text,
                          kb=[[Btn(features.user_leave.button)], [Btn(features.no_state.button)]]))


def user_leave_room(user: User, command: str):
    # если юзер передумал
    if command in features.no_state.activators:
        msg = Message(features.no_state.text)
    else:
        room_id = user.get_user_room_id()
        # пишем админу из чьей комнаты он вышел
        room_admin_id = Users.get_or_none(room_id=room_id, is_admin=True)
        if room_admin_id:
            # пишем админу что из его комнаты вышли
            user_name = vk_methods.linked_user_name(user.uid)
            msg_send.send_msg(user_id=room_admin_id.user_social_id,
                              msg=Message(features.user_leave.text2.format(user_name), kb=[[Btn(features.about.button)]]))
        user.leave_room()
        msg = Message(features.user_leave.text)
    user.drop_state()
    user.send_msg(msg)
    about_response(user)


def state_error(user: User):
    user.drop_state()
    my_name = vk_methods.linked_user_name(settings.error_receiver_id)
    user.send_msg(Message(features.error_state.text.format(my_name)))


def start_gifts_shuffle(admin: User):
    # закольцовываем список участников
    members = [i.user_social_id for i in admin.get_all_room_users()]
    random.shuffle(members)
    members.append(members[0])

    # проверка готовности участников
    for uid_i in range(len(members) - 1):
        user_id = members[uid_i]
        msg_to_user = msg_send.send_msg(user_id=user_id, msg=Message(features.check_shuffle.text))
        if not msg_to_user:
            user_link = vk_methods.linked_user_name(user_id)
            admin.send_msg(Message(f"{user_link} {features.check_shuffle.text2}"))
            return

    for uid_i in range(len(members) - 1):
        sender_id = members[uid_i]
        sender = User(uid=sender_id)
        getter_id = members[uid_i + 1]
        getter_link = vk_methods.linked_user_name(getter_id)
        # подгружаем вишлист
        getter = User(uid=getter_id)
        getter_wishlist = getter.get_wishlist()
        text = f"{getter_link} {features.start_shuffle.text}. {features.start_shuffle.text2} {getter_wishlist}" \
            if getter_wishlist else f"{getter_link} {features.start_shuffle.text}"
        msg = Message(text)
        sender.send_msg(msg)
        sender.send_msg(Message(features.pls_sub.text))
        # запись в базу зашафленных пар
        sender.set_getter_db_id(getter.db_id)

    admin.room_shuffled()


def check_users_in_room(admin: User):
    all_users = list(admin.get_all_room_users())
    admin.send_msg(Message(features.check_room.text))
    for user in all_users:
        user_name = vk_methods.linked_user_name(user.user_social_id)
        kb = [[Btn(f"{features.kick_user.button} {user.user_social_id}")]]
        admin.send_msg(Message(user_name, kb, inline_kb=True))
    about_response(admin)


def wrong_request(user: User):
    msg = Message(features.wrong_command.text, kb=[[Btn(features.rules_and_help.button)], [Btn(features.about.button)]])
    user.send_msg(msg)


def help_request(user: User):
    my_name = vk_methods.linked_user_name(settings.error_receiver_id)
    user.send_msg(Message(features.rules_and_help.text.format(my_name), kb=[[Btn(features.about.button)]]))


def wishlist_menu_response(user: User):
    wish_list = user.get_wishlist()
    msg = Message(f"{features.wish_list_menu.text.format(wish_list=wish_list)}\n", [])
    for ftr in [features.create_wish_list, features.append_wish_list]:
        msg.text += f"\n — {ftr.descr};"
        msg.kb.append([Btn(ftr.button, color=ftr.button_color)])
    msg.kb.append([Btn(features.about.button, color=features.about.button_color)])
    user.send_msg(msg)


def wishlist_append_response(user: User):
    user.set_state(state_key=features.append_wish_list.state_key)
    user.send_msg(Message(features.append_wish_list.text))


def wishlist_create_response(user: User):
    user.set_state(state_key=features.create_wish_list.state_key)
    user.send_msg(Message(features.create_wish_list.text))


def process_append_wish_list(user: User, command: str):
    old_wishlist = user.get_wishlist()
    new_wishlist = f"{old_wishlist}\n{command}"
    user.save_wishlist(new_wishlist)
    user.drop_state()
    updated_wishlist = user.get_wishlist()
    user.send_msg(Message(f"{features.append_wish_list.text2}\n\n{updated_wishlist}",
                          kb=[[Btn(features.wish_list_menu.button)], [Btn(features.about.button)]]))
    live_update_wishlist(user, updated_wishlist)


def process_create_wish_list(user: User, command: str):
    user.save_wishlist(command)
    user.drop_state()
    updated_wishlist = user.get_wishlist()
    user.send_msg(Message(f"{features.create_wish_list.text2}\n\n{updated_wishlist}",
                          kb=[[Btn(features.wish_list_menu.button)], [Btn(features.about.button)]]))
    live_update_wishlist(user, updated_wishlist)


def live_update_wishlist(user: User, getter_wishlist: str):
    sender_db = user.get_sender()
    if sender_db:
        sender = User(uid=sender_db.user_social_id)
        getter_link = vk_methods.linked_user_name(user.uid)
        text = f"{getter_link} {features.live_update_wish_list.text2} {getter_wishlist}"
        sender.send_msg(Message(text, kb=[[Btn(features.about.button)]]))
        user.send_msg(Message(features.live_update_wish_list.text,
                              kb=[[Btn(features.wish_list_menu.button)], [Btn(features.about.button)]]))
