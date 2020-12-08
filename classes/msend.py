from classes import soClass, msgCls, myVkbotClass
from lib import keyboardCreator
from vk.exceptions import VkAPIError
import settings


def send_msg(user_id, social, msg: msgCls.Message):
    if social == soClass.vk_soc:
        send_msg_vk(user_id, msg)


def send_msg_vk(user_id, msg: msgCls.Message):
    vk_methods = myVkbotClass.VkMethods(settings.vk_token, settings.vk_api_version, settings.vk_service_token)
    # если есть клава у сообщения
    if msg.kb:
        msg.kb = keyboardCreator.create_vk_keyboard(msg)

    # если юзер не запретил нам отправлять себе сообщения
    try:
        vk_methods.send_message(user_id, msg.text, msg.kb, msg.attach, msg.dont_parse_links)
    except VkAPIError as e:
        print(e)
