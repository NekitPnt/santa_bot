from classes.featureClass import Feature


about = Feature(
    activators=["начать", "help", "помощь", "привет", "создать свою", "создать", "бот", "старт"],
    prefix="привет",
    text="Добро пожаловать в санта бота! Вы можете создать новую комнату или присоединиться к созданной по ссылке, "
         "которую вам скинет ваш друг.",
    button="В комнату"
)
admin_about = Feature(
    text="Вы админ комнаты и можете:"
)
user_about = Feature(
    text="Вы сейчас в комнате и можете:",
)
room_creation = Feature(
    activators=["создать новую комнату", "-создать новую комнату", "— создать новую комнату"],
    text="Комната создана, чтобы пригласить в нее своих друзей, отправьте им ссылку-приглашение. Также можно "
         "использовать код, для этого его нужно просто отправить мне, или же переслать это сообщение",
    button="Создать комнату",
    descr="Создать новую комнату и пригласить туда друзей"
)
user_adding = Feature(
    text="Добро пожаловать в комнату {0}! Ожидайте когда бот пришлет вам случайного получателя подарка.",
    prefix="join"
)
user_leave = Feature(
    text="Вы вышли из комнаты, теперь можете создать свою или присоединиться к созданной по ссылке.",
    button="Выйти из комнаты",
    descr="Выйти из комнаты"
)
kick_user = Feature(
    text="Пользователь {0} был выгнан из комнаты",
    button="Выгнать",
    descr="Выгнать пользователя из комнаты",
    prefix="выгнать"
)
start_shuffle = Feature(
    text="найдет ваш подарок под ёлкой",
    button="Провести жеребьевку",
    descr="Провести жеребьевку"
)
reshuffle = Feature(
    button="Перебросить жребий",
    descr="Провести жеребьевку заново (вдруг кто-то очень недоволен)"
)
check_room = Feature(
    text="Сейчас в вашей комнате эти люди",
    button="Участники",
    descr="Посмотреть список всех друзей в комнате. Если кто-то из них вам больше не друг, его можно выгнать"
)
delete_room = Feature(
    text="Комната удалена насовсем",
    button="Удалить комнату",
    button_color="red",
    descr="Удалить комнату насовсем"
)
room_error = Feature(
    text="Такой комнаты не существует, попробуйте еще раз"
)
sucseed_shuffle = Feature(
    text="Жеребьевка прошла успешно!"
)
access_error = Feature(
    text="Доступ ограничен: Вы не админ комнаты"
)
kicked_user = Feature(
    text="Увы и ах, но вас, к сожалению, выгнали из комнаты"
)
pls_sub = Feature(
    text="Если вам понравился наш бот, не забывайте подписываться на него, чтобы не пропускать новые крутые фичи!"
)
wrong_command = Feature(
    text="Я простой бот и понимаю только определенные команды. По всем вопросам пишите {0}"
)
aaaaaaaaa = Feature(
    activators=[],
    text="",
    button="",
    descr=""
)
