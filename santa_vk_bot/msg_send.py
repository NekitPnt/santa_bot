import json
from vk.exceptions import VkAPIError

from santa_vk_bot.config import settings
from santa_vk_bot.classes import myVkbotClass, msgCls


def send_msg(*, user_id, msg: msgCls.Message):
    send_msg_vk(user_id, msg)


def send_msg_vk(user_id, msg: msgCls.Message):
    vk_methods = myVkbotClass.VkMethods(settings.vk_bot_token, settings.vk_api_version, settings.vk_service_token)
    # если есть клава у сообщения
    if msg.kb:
        msg.kb = create_vk_keyboard(msg)

    # если юзер не запретил нам отправлять себе сообщения
    try:
        vk_methods.send_message(user_id, msg.text, msg.kb, msg.attach, msg.dont_parse_links)
    except VkAPIError as e:
        print(e)


def create_vk_keyboard(msg):
    """
    Стандартное отображение
    По умолчанию, если не передан параметр inline, клавиатура показывается под полем ввода в диалоге с пользователем.
    Максимальный размер стандартной клавиатуры — 5 × 10. Максимальное количество клавиш: 40.

    Inline-отображение
    Клавиатура может отображаться внутри сообщения — это inline-отображение. Чтобы включить его, передайте параметр
    inline в объект клавиатуры. Её максимальный размер составит 5 × 6. Максимальное количество клавиш: 10.
    """
    one_time_flag = not msg.inline_kb
    btn_colors = {
        'white': 'default',
        'blue': 'primary',
        'red': 'negative',
        'green': 'positive'
    }
    button_rows = []
    for rows in msg.kb:
        if rows:
            row = []
            for btn in rows:
                payload = btn.payload.to_dict() if btn.payload else json.dumps({"command": btn.label})
                color = btn_colors[btn.color] if btn.color else btn_colors['white']
                if btn.url:
                    payload = json.dumps({"payload": btn.url})
                    row.append({'action': {'type': 'open_link', 'link': btn.url, 'payload': payload, 'label': btn.label}})
                elif msg.callback_kb:
                    row.append({'action': {'type': 'callback', 'payload': payload, 'label': btn.label}, 'color': color})
                else:
                    row.append({'action': {'type': 'text', 'payload': payload, 'label': btn.label}, 'color': color})
            button_rows.append(row)
    keyboard = {'one_time': one_time_flag, 'buttons': button_rows, 'inline': msg.inline_kb}

    return keyboard

    # example
    # print(create_keyboard(False, [[['text1'], ['text2','blue']], [['text3','red','123']],
    #                               [['text3','','', 'google.com']]]))
