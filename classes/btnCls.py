from dataclasses import dataclass
from . import payloadClass


@dataclass
class Btn:
    label: str
    color: str = ""
    payload: payloadClass.Payload = None
    url: str = ""
