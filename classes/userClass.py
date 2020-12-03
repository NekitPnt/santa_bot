from classes import soClass, msgCls, myVkbotClass
from lib import keyboardCreator
from models import Users, Rooms
from vk.exceptions import VkAPIError
import settings
import utils


class User:
    def __init__(self, social: soClass.Socials, data: dict = None, uid: str = None):
        if data:
            self.uid: str = data['from_id'] if social == soClass.vk_soc else data['chat']['id']
        else:
            self.uid: str = uid
        self.social = social
        self.db_id = self.get_or_create_user()
        self.is_admin = False
        self.room_id = self.get_user_room_id()

    def get_or_create_user(self) -> int:
        user, created = Users.get_or_create(user_social_id=self.uid, social=self.social.key)
        self.is_admin = user.is_admin
        return user.id

    def get_user_room_id(self) -> int:
        return Users.get_or_none(id=self.db_id).room_id

    def get_room_shuffled(self):
        if self.room_id:
            return Rooms.get_or_none(room_id=self.room_id).shuffled

    def room_shuffled(self):
        Rooms.update(shuffled=True).where(room_id=self.room_id).execute()

    def create_room(self):
        if self.room_id:
            return self.room_id
        else:
            self.room_id = Rooms.create().id
            Users.update(room_id=self.room_id, is_admin=True).where(Users.id == self.db_id).execute()
            return self.room_id

    def set_room(self, room_id):
        self.room_id = room_id
        Users.update(room_id=self.room_id).where(Users.id == self.db_id).execute()

    def leave_room(self):
        self.room_id = None
        Users.update(room_id=None).where(Users.id == self.db_id).execute()

    def get_all_room_users(self):
        return Users.select().where(Users.room_id == self.room_id)

    def kick_user(self, user_db_id):
        Users.update(room_id=None).where((Users.room_id == self.room_id) & Users.id == user_db_id).execute()

    def clear_room(self) -> list:
        in_room_users = self.get_all_room_users()
        all_room_users_ids = []
        for user in in_room_users:
            all_room_users_ids.append(user.room_id)
            Users.update(room_id=None).where(Users.id == user.id).execute()
        return all_room_users_ids

    def send_msg(self, msg: msgCls.Message):
        if self.social == soClass.vk_soc:
            self.send_msg_vk(msg)

    def send_msg_vk(self, msg: msgCls.Message):
        vk_methods = myVkbotClass.VkMethods(settings.vk_token[settings.prod], settings.vk_api_version, settings.vk_service_token)
        # если есть клава у сообщения
        # if msg.kb:
          #   msg.kb = keyboardCreator.create_vk_keyboard(msg)

        # если юзер не запретил нам отправлять себе сообщения
        try:
            vk_methods.send_message(self.uid, msg.text, msg.kb, msg.attach, msg.dont_parse_links)
        except VkAPIError as e:
            print(e)
