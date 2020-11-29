from dataclasses import dataclass, field
from typing import List
from classes.soClass import Socials


@dataclass
class Message:
    text: str = ""
    kb: List[List[List[str]]] = None
    attach: list = field(default_factory=list)
    social: Socials = None
