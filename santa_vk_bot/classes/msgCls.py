from dataclasses import dataclass, field
from typing import List
from . import payloadClass


@dataclass
class Btn:
    label: str
    color: str = ""
    payload: payloadClass.Payload = None
    url: str = ""


@dataclass
class Message:
    text: str = ""
    kb: List[List[Btn]] = None
    attach: list = field(default_factory=list)
    inline_kb: bool = False
    callback_kb: bool = False
    parse_mode: str = ''
    dont_parse_links: int = 1