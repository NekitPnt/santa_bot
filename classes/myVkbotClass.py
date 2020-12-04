import json
import os
import requests
import vk


class VkMethods:
    def __init__(self, token, api_version, service_token=''):
        self.session = vk.Session()
        self.api = vk.API(self.session, v=api_version)
        self.token = token
        self.service_token = service_token

    def send_message(self, user_id, message="", keyboard=None, attachment=(), dont_parse_links=1):
        if keyboard is None:
            keyboard = {'one_time': True, 'buttons': []}
        # отображение русских клавиш
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-16', 'surrogatepass').decode('utf-16')

        self.api.messages.send(access_token=self.token, user_id=user_id, message=message, keyboard=keyboard,
                               attachment=attachment, dont_parse_links=dont_parse_links)

    def edit_message(self, user_id, message_id, new_text, keyboard=None):
        if keyboard is None:
            keyboard = {'one_time': True, 'buttons': []}
        # отображение русских клавиш
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-16', 'surrogatepass').decode('utf-16')
        self.api.messages.edit(access_token=self.token, peer_id=user_id,
                               conversation_message_id=message_id, message=new_text, keyboard=keyboard)

    def massive_send_message(self, user_ids, message="", keyboard=None, attachment=(), dont_parse_links=1):
        if keyboard is None:
            keyboard = {'one_time': True, 'buttons': []}
        # отображение русских клавиш
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-16', 'surrogatepass').decode('utf-16')

        self.api.messages.send(access_token=self.token, user_ids=user_ids, message=message,
                               keyboard=keyboard, attachment=attachment, dont_parse_links=dont_parse_links)

    def send_message_to_chat(self, peer_id, message="", attachment=()):
        self.api.messages.send(access_token=self.token, peer_id=peer_id, message=message, attachment=attachment)

    def set_activity(self, user_id, group_id, activity_type='typing'):
        self.api.messages.setActivity(access_token=self.token, user_id=user_id, type=activity_type, group_id=group_id)

    def execute(self, code):
        return self.api.execute(access_token=self.token, code=code)

    def send_message_event_answer(self, event_id, user_id, peer_id="", event_data=None):
        self.api.messages.sendMessageEventAnswer(access_token=self.token, event_id=event_id, user_id=user_id,
                                                 peer_id=peer_id, event_data=event_data)

    def check_user_sub(self, group_id, user_id):
        return self.api.groups.isMember(access_token=self.token, group_id=group_id, user_id=user_id)['member']

    def photo_by_id(self, photo_id):
        return self.api.photos.getById(access_token=self.service_token, photos=photo_id)[0]

    def count_wall_posts(self, group_id):
        return self.api.wall.get(access_token=self.service_token, owner_id=group_id, count=1)["count"]

    def is_messages_allowed(self, group_id, user_id):
        return self.api.messages.isMessagesFromGroupAllowed(
            access_token=self.token, group_id=group_id, user_id=user_id)['is_allowed']

    def upload_doc_for_vk(self, peer_id, file_path, title):
        file = requests.post(
            self.api.docs.getMessagesUploadServer(access_token=self.token, peer_id=peer_id)['upload_url'],
            files={'file': open(file_path, 'rb')}).json()
        doc = self.api.docs.save(access_token=self.token, file=file['file'], title=title)[0]
        att = 'doc%s_%s' % (peer_id, doc['id'])

        return att

    def upload_photo_for_vk(self, peer_id, proxy_file_path):
        file = requests.post(
            self.api.photos.getMessagesUploadServer(access_token=self.token, peer_id=peer_id)['upload_url'],
            files={'photo': open(proxy_file_path, 'rb')}).json()
        photo = self.api.photos.saveMessagesPhoto(access_token=self.token, server=file['server'],
                                                  photo=file['photo'], hash=file['hash'])[0]
        att = 'photo%s_%s' % (peer_id, photo['id'])
        os.remove(os.path.abspath(proxy_file_path))

        return att

    def get_group_wall(self, group_id, size=None, shift=0):
        if size is None:
            size = self.api.wall.get(access_token=self.service_token, owner_id=group_id, count=1)["count"]
        c = size//100 + 1
        result = []
        for i in range(c):
            d = self.api.wall.get(access_token=self.service_token, owner_id=group_id, offset=i*100+shift, count=100)
            for j in d['items']:
                if len(result) < size:
                    result.append(j)

        return result

    def user_get(self, user_ids, fields=''):
        return self.api.users.get(access_token=self.token, user_ids=user_ids, fields=fields)

    def user_name(self, user_id) -> dict:
        # [{'id': id, 'first_name': 'Name', 'last_name': 'Lname'}]
        return self.api.users.get(access_token=self.token, user_ids=user_id)[0]

    def linked_user_name(self, user_id):
        full_name = self.user_name(user_id)
        linked_name = f"@id{user_id}({full_name['first_name']} {full_name['last_name']})"
        return linked_name

    def widgets_get_pages(self, widget_api_id: int, order: str = 'date', period: str = 'alltime', offset: int = 0, count: int = 10):
        return self.api.widgets.getPages(access_token=self.service_token, widget_api_id=widget_api_id, order=order,
                                         period=period, offset=offset, count=count)

    def widgets_get_comments(self, widget_api_id: int, url: str, page_id: str, order: str = 'date', fields: str = '', offset: int = 0, count: int = 10):
        return self.api.widgets.getComments(access_token=self.service_token, widget_api_id=widget_api_id, url=url,
                                            page_id=page_id, order=order, fields=fields, offset=offset, count=count)

    def create_comment(self, owner_id, post_id, from_group, message, reply_to_comment):
        self.api.wall.createComment(access_token=self.token, owner_id=owner_id, post_id=post_id,
                                    from_group=from_group, message=message, reply_to_comment=reply_to_comment)
