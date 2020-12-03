from dataclasses import dataclass


@dataclass
class Btn:
    label: str
    color: str = ""
    payload: str = ""
    url: str = ""
