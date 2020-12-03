from dataclasses import dataclass, field
from typing import List
from . import btnCls


@dataclass
class Message:
    text: str = ""
    kb: List[List[List[btnCls.Btn]]] = None
    attach: list = field(default_factory=list)
    inline_kb: bool = False
    callback_kb: bool = False
    parse_mode: str = ''
    dont_parse_links: int = 1
