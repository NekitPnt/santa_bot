from typing import List
from classes import accessClass, statClass, soClass, userClass
from modules import statCollector

default_sub_checkbox = "☑️ "


class Feature:
    all_activators = []
    all_prefixes = []
    all_instances = []
    active_instances = []

    def __init__(self, activators: List[str] = None, title: str = "", stat: statClass.StatField = None,
                 button: str = None, text: str = "", descr: str = "", prefix: str = "", ftr_lock_key: str = "",
                 social: List[soClass.Socials] = (soClass.vk_soc, soClass.tg_soc), button_color: str = "white",
                 access: accessClass.AccessType = accessClass.user_access, funct: any = None, db_key: str = "",
                 ignore_duplic: bool = False, button_url: str = "", disabled: bool = False, cache_key: str = ""):
        self.activators = activators if activators else []  # дословные команды активации
        self.title = title  # заголовок для фичи
        self.stat = stat  # поле с инфой по стате
        self.prefix = prefix  # префиксные команды активации
        self.ftr_lock_key = ftr_lock_key  # ключевое слово для блокировки юзера на фиче
        self.button = button  # набор вариантов текстов кнопки
        self.button_color = button_color  # цвет кнопки
        self.descr = descr  # описание фичи для меню в котором она находится
        self.text = text  # какой-либо текст сообщения для фичи, как правило описание верхнего уровня
        self.social = social  # для каких платформ должна работать фича
        self.access = access  # уровни доступа - юзер или админ
        self.db_key = db_key  # ключ для базы данных
        self.funct = funct  # функция-обработчик фичи
        self.button_url = button_url  # ссылка для кнопки-ссылки
        self.disabled = disabled  # нужно ли отключить фичу
        self.cache_key = cache_key  # ключ фичи в кэше
        # ниже проверяем активаторы и префиксы на отсутсвие пересечений
        if button:
            self.activators.append(button.lower())
        if activators:
            # для каждого активатора добавляем слэш в начале
            self.activators += [f"/{i}" for i in activators]
            if not ignore_duplic:
                duplic_act = [x in Feature.all_activators for x in self.activators]
                if any(duplic_act):
                    raise ValueError(
                        f"Duplicate activators {[activators[_] for _ in range(len(duplic_act)) if duplic_act[_]]}")
                Feature.all_activators.extend(self.activators)
            if prefix:
                if prefix in Feature.all_prefixes:
                    raise ValueError(f"Duplicate prefixes {prefix}")
                Feature.all_prefixes.append(self.prefix)
        # добавляем фичу в список активных фичей если она не disabled
        if not self.disabled:
            self.__class__.active_instances.append(self)

    def stata_wrapper(self, func):
        def stat_collect(**kwargs):
            if self.stat:
                statCollector.stat_collector(kwargs['user'], self.stat)
            return func(**kwargs)

        return stat_collect

    def simple_stat_collect(self, user: userClass.User):
        if self.stat:
            statCollector.stat_collector(user, self.stat)

    @staticmethod
    def act_list(ftr_list: list) -> List[str]:
        return [act for feature in ftr_list for act in feature.activators]

    @classmethod
    def get_active_db_key_ftr_map(cls, feature_db_key: str = None):
        if feature_db_key:
            return {feature.db_key: feature for feature in cls.active_instances}[feature_db_key]
        else:
            return {feature.db_key: feature for feature in cls.active_instances}

    @classmethod
    def get_all_db_key_ftr_map(cls, feature_db_key: str = None):
        if feature_db_key:
            return {feature.db_key: feature for feature in cls.all_instances}[feature_db_key]
        else:
            return {feature.db_key: feature for feature in cls.all_instances}

    @classmethod
    def get_active_command_ftr_map(cls, command: str = None):
        if command:
            return {act: feature for feature in cls.active_instances for act in feature.activators}[command]
        else:
            return {act: feature for feature in cls.active_instances for act in feature.activators}

    @classmethod
    def active_act_list(cls) -> List[str]:
        return [act for feature in cls.active_instances for act in feature.activators]

    @classmethod
    def active_db_key_list(cls) -> List[str]:
        return [feature.db_key for feature in cls.active_instances]


class MailingTag(Feature):
    all_instances = []
    active_instances = []

    def __init__(self, activators: List[str] = None, title: str = "", stat: statClass.StatField = None,
                 button: str = None, text: str = "", descr: str = "", prefix: str = "", ftr_lock_key: str = "",
                 social: List[soClass.Socials] = (soClass.vk_soc, soClass.tg_soc), button_color: str = "white",
                 access: accessClass.AccessType = accessClass.user_access, funct: any = None,
                 ignore_duplic: bool = False, button_url: str = "", disabled: bool = False,
                 sub_checkbox: str = default_sub_checkbox,
                 is_service: bool = False, db_key: str = "", wp_site_db_slug: List[str] = None):
        self.sub_checkbox = sub_checkbox  # эмоджи которое означает подписку
        self.is_service = is_service  # сервисная рассылка не для всех юзеров
        self.wp_site_db_slug = wp_site_db_slug  # ключ рассылки в базе сайта
        self.__class__.all_instances.append(self)  # добавляем инстанс в список
        Feature.__init__(self, activators=activators, title=title, stat=stat, button=button, text=text, descr=descr,
                         prefix=prefix, ftr_lock_key=ftr_lock_key, social=social, button_color=button_color,
                         access=access, funct=funct, db_key=db_key, ignore_duplic=ignore_duplic, button_url=button_url,
                         disabled=disabled)

    @classmethod
    def create_interests_kb(cls, user_interests: list, all_tags_ftr):
        kb = []
        row = []
        if not user_interests:
            user_interests = []
        for feature in cls.active_instances:
            if feature is not all_tags_ftr:
                button = f"{feature.sub_checkbox} {feature.button}" if feature.db_key in user_interests else feature.button
                row.append([button])
                if len(row) > 2:
                    kb.append(row)
                    row = []
        if row:
            kb.append(row)
        kb.append([[f"{all_tags_ftr.sub_checkbox} {all_tags_ftr.button}"
                    if all_tags_ftr.db_key in user_interests else all_tags_ftr.button]])
        return kb

    @classmethod
    def interests_as_tags(cls, user_interests: list) -> list:
        """user_interests_as_tags = List[MailingTag.db_key]"""
        res = []
        for ftr_db_key, feature in cls.get_all_db_key_ftr_map().items():
            if ftr_db_key in user_interests:
                res.extend(feature.wp_site_db_slug)
        return res


class MailingChannel(Feature):
    all_instances = []
    active_instances = []

    def __init__(self, activators: List[str] = None, title: str = "", stat: statClass.StatField = None,
                 button: str = None, text: str = "", descr: str = "", prefix: str = "", ftr_lock_key: str = "",
                 social: List[soClass.Socials] = (soClass.vk_soc, soClass.tg_soc), button_color: str = "white",
                 access: accessClass.AccessType = accessClass.user_access, funct: any = None, header: str = "",
                 ignore_duplic: bool = False, button_url: str = "", disabled: bool = False, interests: bool = True,
                 auto_mailing_trigger: str = "", is_service: bool = False, titlemoji: str = "",
                 sub_checkbox: str = default_sub_checkbox, db_key: str = "", wp_site_db_slug: List[str] = None):
        self.sub_checkbox = sub_checkbox  # эмоджи которое означает подписку
        self.header = header  # хедер для рассылок
        self.interests = interests  # доступен ли выбор интересов для этого канала
        self.auto_mailing_trigger = auto_mailing_trigger  # триггер для авторассылок
        self.is_service = is_service  # сервисная рассылка не для всех юзеров
        self.wp_site_db_slug = wp_site_db_slug  # ключ рассылки в базе сайта
        self.titlemoji = titlemoji
        self.__class__.all_instances.append(self)  # добавляем инстанс в список
        Feature.__init__(self, activators=activators, title=title, stat=stat, button=button, text=text, descr=descr,
                         prefix=prefix, ftr_lock_key=ftr_lock_key, social=social, button_color=button_color,
                         access=access, funct=funct, db_key=db_key, ignore_duplic=ignore_duplic, button_url=button_url,
                         disabled=disabled)

    @classmethod
    def get_channel_from_wp_slug(cls, wp_site_db_slug: str):
        ftr_map = {tag: feature
                   for feature in cls.active_instances
                   if feature.wp_site_db_slug
                   for tag in feature.wp_site_db_slug}
        return ftr_map[wp_site_db_slug] if wp_site_db_slug in ftr_map else None
