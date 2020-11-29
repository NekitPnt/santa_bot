from dataclasses import dataclass
import json


@dataclass
class Payload:
    command: str = ""
    channel: str = ""
    edit_msg: str = ""
    post_id: str = ""
    answ_back: int = 0
    button_type: str = ""
    payload: str = ""

    def to_dict(self):
        dicted_payload = self.__dict__
        res = {}
        for k, v in dicted_payload.items():
            if v:
                res.update({k: v})
        return json.dumps(res, ensure_ascii=False)


def get_payload(payload):
    try:
        if type(payload) == dict:
            return Payload(**payload)
        return Payload(**json.loads(payload))
    except json.decoder.JSONDecodeError:
        return None
