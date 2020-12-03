from dataclasses import dataclass


@dataclass(frozen=True)
class Socials:
    key: str
    name: str = ''


vk_soc = Socials(key='vk', name='VK')
tg_soc = Socials(key='tg', name='Telegram')
