from classes import soClass, msgCls, msend
from models import Users, Rooms


class User:
    def __init__(self, social: soClass.Socials, data: dict = None, uid: str = None):
        if data:
            self.uid: str = data['from_id'] if social == soClass.vk_soc else data['chat']['id']
        else:
            self.uid: str = uid
        self.social = social
        self.is_admin = False
        self.db_id = self.get_or_create_user()
        self.room_id = self.get_user_room_id()

    def get_or_create_user(self) -> int:
        user, created = Users.get_or_create(user_social_id=self.uid, social=self.social.key)
        self.is_admin = user.is_admin
        return user.id

    def get_user_room_id(self) -> int:
        return Users.get_or_none(id=self.db_id).room_id

    def get_room_shuffled(self):
        if self.room_id:
            return Rooms.get_or_none(id=self.room_id).shuffled

    def room_shuffled(self):
        Rooms.update(shuffled=True).where(Rooms.id == self.room_id).execute()

    def create_room(self):
        if self.room_id:
            return self.room_id
        else:
            self.room_id = Rooms.create().id
            Users.update(room_id=self.room_id, is_admin=True).where(Users.id == self.db_id).execute()
            self.is_admin = True
            return self.room_id

    def set_room(self, room_id):
        room = Rooms.get_or_none(id=room_id)
        # если у чела уже есть комната говорим ему об этом
        if self.room_id == room_id:
            return 'exists'
        # если комната существует
        if room:
            self.room_id = room_id
            Users.update(room_id=self.room_id, is_admin=False).where(Users.id == self.db_id).execute()
            return room_id
        return 0

    def leave_room(self):
        self.room_id = None
        Users.update(room_id=None, is_admin=False).where(Users.id == self.db_id).execute()

    def get_all_room_users(self):
        return Users.select().where(Users.room_id == self.room_id)

    @staticmethod
    def kick_user(user_db_id):
        Users.update(room_id=None, is_admin=False).where(Users.id == user_db_id).execute()

    def clear_room(self) -> list:
        in_room_users = self.get_all_room_users()
        all_room_users_ids = []
        for user in in_room_users:
            all_room_users_ids.append(user.user_social_id)
            Users.update(room_id=None, is_admin=False).where(Users.id == user.id).execute()
        self.room_id = None
        self.is_admin = False
        return all_room_users_ids

    def send_msg(self, msg: msgCls.Message):
        msend.send_msg(self.uid, self.social, msg)

    def save_wishlist(self, wishlist: str):
        Users.update(wish_list=wishlist).where(Users.id == self.db_id).execute()

    def get_wishlist(self):
        return Users.get(id=self.db_id).wish_list
