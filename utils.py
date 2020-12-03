from classes import userClass, soClass, msgCls
import settings


# функция уведомляющая админа об ошибке
def error_notificator(error: any):
    error = str(error)
    print(error)
    try:
        admin = userClass.User(soClass.vk_soc, uid=settings.error_receiver_id)
        admin.send_msg(msgCls.Message(error))
    except Exception as e:
        print(f'Error in error_notificator: {e}')


"""def msg_allowed(user_db_key: str, redis_db: redisClass.MyRedis, social: soClass.Socials = None):
    user_data = redis_db.get_dict(user_db_key)
    if user_data:
        user_data['message_allow'] = 1
        redis_db.set_dict(user_db_key, user_data)


def msg_denied(user_db_key: str, redis_db: redisClass.MyRedis, social: soClass.Socials = None):
    user_data = redis_db.get_dict(user_db_key)
    if user_data:
        user_data['message_allow'] = 0
        redis_db.set_dict(user_db_key, user_data)"""
