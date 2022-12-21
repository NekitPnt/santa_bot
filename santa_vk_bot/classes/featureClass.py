class Feature:
    def __init__(
            self,
            activators: list[str] = None,
            button: str = None,
            text: str = "",
            text2: str = "",
            descr: str = "",
            prefix: str = "",
            button_color: str = "white",
            state_key: str = "",
    ):
        self.activators = activators if activators else []  # дословные команды активации
        self.prefix = prefix  # префиксные команды активации
        self.button = button  # набор вариантов текстов кнопки
        self.button_color = button_color  # цвет кнопки
        self.descr = descr  # описание фичи для меню в котором она находится
        self.text = text  # какой-либо текст сообщения для фичи, как правило описание верхнего уровня
        self.text2 = text2  # какой-либо текст сообщения для фичи, как правило описание верхнего уровня
        self.state_key = state_key  # локер для стейта
        # ниже проверяем активаторы и префиксы на отсутсвие пересечений
        if button:
            self.activators.append(button.lower())
        if activators:
            # для каждого активатора добавляем слэш в начале
            self.activators += [f"/{i}" for i in activators]
