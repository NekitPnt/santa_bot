from dataclasses import dataclass


@dataclass
class AccessType:
    key: str
    name: str = ""


user_access = AccessType(key="user")
admin_access = AccessType(key="admin")
