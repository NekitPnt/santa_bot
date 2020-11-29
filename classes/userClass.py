from classes import soClass, redisClass


class User:
    def __init__(self, uid: str, user_db_id: int, redis_db: redisClass.MyRedis,
                 social: soClass.Socials, is_admin: bool = False):
        self.uid: str = str(uid)
        self.user_db_id: int = user_db_id
        self.redis_db = redis_db
        self.social = social
        self.is_admin = is_admin
        self.data = self.get_data()

    def get_data(self) -> dict:
        return self.redis_db.get_dict(self.uid)

    def set(self, user_data: dict):
        self.redis_db.set_dict(self.uid, user_data)

    def save(self):
        self.redis_db.set_dict(self.uid, self.data)

    def release_ftr_lock(self):
        self.data['in_feature'] = "0"
        self.save()

    def check_in_ftr(self, condition):
        return self.data['in_feature'] == condition

    def lock_on_ftr(self, lock_key: str):
        if not lock_key:
            raise KeyError("Empty lock_key field")
        self.data['in_feature'] = lock_key
        self.save()

    def drop_cache_field(self, cache_key: str):
        if self.data['cache'].get(cache_key, None):
            self.data['cache'].pop(cache_key)
            self.save()
        else:
            raise KeyError("Empty cache field")

    def get_cache(self, cache_key: str):
        return self.data['cache'].get(cache_key, None)

    def set_cache(self, cache_key: str, cache_value):
        if 'cache' not in self.data:
            self.data['cache'] = {}
        self.data['cache'].update({cache_key: cache_value})
        self.save()
