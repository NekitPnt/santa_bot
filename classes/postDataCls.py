from dataclasses import dataclass, field


@dataclass
class SitePostData:
    category: str = ""
    tags: list = field(default_factory=list)
    tags_names: list = field(default_factory=list)
    title: str = ""
    descr: str = ""
    name: str = ""


@dataclass
class MetaPostData:
    post_id: int = 0
    title: str = ""
    tags_footer: str = ""
    vk_link: str = ""
    tg_link: str = ""
    attachments: str = ""
    bot_keyboard: str = ""


@dataclass
class MailingCreationStep:
    key: str
    name: str
    default: str
    instruction: str = ''
