class Feature:
    def __init__(
            self,
            activators: list[str] = None,
            button: str = None,
            text: str = "",
            descr: str = "",
            prefix: str = "",
            button_color: str = "white",
            db_key: str = "",
    ):
        self.activators = activators if activators else []  # дословные команды активации
        self.prefix = prefix  # префиксные команды активации
        self.button = button  # набор вариантов текстов кнопки
        self.button_color = button_color  # цвет кнопки
        self.descr = descr  # описание фичи для меню в котором она находится
        self.text = text  # какой-либо текст сообщения для фичи, как правило описание верхнего уровня
        self.db_key = db_key  # ключ для базы данных
        # ниже проверяем активаторы и префиксы на отсутсвие пересечений
        if button:
            self.activators.append(button.lower())
        if activators:
            # для каждого активатора добавляем слэш в начале
            self.activators += [f"/{i}" for i in activators]
