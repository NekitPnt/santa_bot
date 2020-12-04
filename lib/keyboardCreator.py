from telebot import types
from typing import List
import json

from classes.payloadClass import Payload


def create_payload(element: any):
    return json.dumps(element, ensure_ascii=False) \
                        if type(element) is dict else json.dumps({"command": element}, ensure_ascii=False)


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
                import utils
                utils.error_notificator(btn)
                payload = btn.payload.to_dict() if btn.payload else json.dumps({"command": btn.label})
                color = btn.color if btn.color else btn_colors['white']
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


# создаватель клавы для телеги
def create_tg_keyboard(keyboard, inline_kb):
    if not keyboard:
        keyboard_markup = types.ReplyKeyboardRemove()
    elif inline_kb:
        keyboard_markup = types.InlineKeyboardMarkup()
        for i in keyboard:
            if i:
                row = []
                for j in i:
                    if len(j) in [1, 2]:
                        callback_data = Payload(j[0]).to_dict()
                        row.append(types.InlineKeyboardButton(str(j[0]), callback_data=callback_data))
                    elif len(j) == 3:
                        callback_data = j[2]
                        row.append(types.InlineKeyboardButton(str(j[0]), callback_data=callback_data))
                    elif len(j) == 4:
                        row.append(types.InlineKeyboardButton(str(j[0]), url=j[3]))
                keyboard_markup.row(*row)
    else:
        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        # [[['a'], ['b']], [['c']]]
        for i in keyboard:
            if i:
                keyboard_markup.row(*[str(j[0]) for j in i])

    return keyboard_markup


def text_to_keyboard_converter(text: str) -> List[List[List[str]]]:
    keyboard: list = text.split('\n')
    for i in range(len(keyboard)):
        keyboard[i] = keyboard[i].split('///')
    for i in range(len(keyboard)):
        if len(keyboard[i]) == 1:
            if len(keyboard[i][0]) > 38:
                raise ValueError(f"Too long button text")
            else:
                # добавляем кнопку в ряд если она одна
                if all(br in keyboard[i][0] for br in ['(', ')']):
                    url_button = get_button_url_from_brackets(keyboard[i][0])
                    keyboard[i][0] = [url_button['button_title'], '', '', url_button['url']]
                else:
                    keyboard[i] = [keyboard[i]]
        elif 1 < len(keyboard[i]) <= 4:
            for j in range(len(keyboard[i])):
                if len(keyboard[i][j]) > 38:
                    raise ValueError(f"Too long button text")
                else:
                    if all(br in keyboard[i][j] for br in ['(', ')']):
                        if len(keyboard[i]) > 2:
                            raise ValueError(f"Only ONE url-button in a row")
                        else:
                            url_button = get_button_url_from_brackets(keyboard[i][j])
                            keyboard[i][j] = [url_button['button_title'], '', '', url_button['url']]
                    else:
                        keyboard[i][j] = [keyboard[i][j]]
        else:
            raise ValueError(f"Too long button row, must be 1 < . < 4")

    return keyboard


# парсер текстового представления урловой кнопки
def get_button_url_from_brackets(string: str) -> dict:
    url = string[string.find("(") + 1: string.rfind(")")]
    button_title = string.replace('(' + url + ')', '')
    if not any(http in url for http in ['http://', 'https://']):
        url = 'http://' + url
    return {'button_title': button_title, 'url': url}


# обрезальщик инлайн клавиатуры для вк
def kb_cutter(kb) -> list:
    button_sum = 10
    new_buttons_sum = 0
    new_kb = []
    new_kbs = []
    for button_row in kb:
        new_buttons_sum += len(button_row)
        if new_buttons_sum < button_sum:
            new_kb.append(button_row)
        else:
            new_kbs.append(new_kb)
            new_kb = [button_row]
            new_buttons_sum = len(button_row)
    if new_kb:
        new_kbs.append(new_kb)
    return new_kbs


def quizzes_kb(buttons: List[list]) -> List[List[list]]:
    row_limit = 4
    kb = []
    row = []
    for button in buttons:
        if len(row) < row_limit:
            row.append(button)
        else:
            kb.append(row)
            row = [button]
    if row:
        kb.append(row)
    return kb
