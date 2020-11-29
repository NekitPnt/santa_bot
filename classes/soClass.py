from dataclasses import dataclass


@dataclass(frozen=True)
class SocPlatform:
    key: str
    name: str = ''
    descr: str = ''


VK = SocPlatform('vk')
TG = SocPlatform('tg')


@dataclass(frozen=True)
class Socials:
    key: str
    name: str = ''
    descr: str = ''
    platform: SocPlatform = VK


vk_soc = Socials(key='vk', name='VK', platform=VK)
tg_soc = Socials(key='tg', name='Telegram', platform=TG)
vk_wp_soc = Socials(key='vk_wp', name='VKontakte Web Page', descr='vk', platform=VK)
tg_wp_soc = Socials(key='tg_wp', name='Telegram Web Page', descr='tg', platform=TG)
