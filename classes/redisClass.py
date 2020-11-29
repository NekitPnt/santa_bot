import redis
import json
import pickle


class MyRedis(redis.Redis):
    def __init__(self, host='localhost', port=6379, db_num=0, password=''):
        # инициализация - подключаемся к базе данных redis на локальном хосте
        # используя один коннекшен пул для реализации паттерна синглтон
        pool = redis.ConnectionPool(host=host, port=port, db=db_num, password=password)
        super().__init__(connection_pool=pool)

    def set_list(self, key: str, array: list):
        redis.Redis.set(self, key, pickle.dumps(array))

    def get_list(self, key: str) -> list:
        result = redis.Redis.get(self, key)
        if result is not None:
            result = pickle.loads(result)
        return result

    def set_dict(self, key: str, dictionary: dict):
        redis.Redis.set(self, key, pickle.dumps(dictionary))

    def get_dict(self, key: str) -> dict:
        # получаем строку-словарь по ключу key и декодируем его в словарь питона
        result = redis.Redis.get(self, key)
        if result is not None:
            # переделываем старый способ сериализации, оставляя поддержку легаси
            try:
                result = pickle.loads(result)
            except pickle.UnpicklingError:
                result = result.decode('utf-8')
                result = result.replace("\\U", "U")
                result = json.loads(result.replace("'", '"'))
        return result
