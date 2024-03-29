from santa_vk_bot.classes.featureClass import Feature


yes_state = Feature(
    button="Да"
)
no_state = Feature(
    button="Нет",
    text="Окей, возвращаюсь в меню"
)
error_state = Feature(
    text="Произошла ошибка внутреннего стейта. Обратитесь за помощью к создателю бота: {0}"
)
about = Feature(
    activators=["начать", "привет", "создать свою", "создать", "бот", "старт"],
    prefix="привет",
    text="Добро пожаловать в санта бота! Вы можете создать новую комнату или присоединиться к созданной по ссылке, "
         "которую вам скинет ваш друг.",
    button="В комнату"
)
admin_about = Feature(
    text="Вы админ комнаты и можете:"
)
user_about = Feature(
    text="Вы сейчас в комнате {admin_name} и можете:",
)
wish_list_menu = Feature(
    prefix="вишлист",
    descr="Создать/дополнить вишлист, чтобы человек, которому вы выпали, точно знал что подарить.",
    button="Вишлист",
    text="Ваш текущий вишлист:\n\n{wish_list}\n\nВот что вы можете сделать:"
)
live_update_wish_list = Feature(
    text="Отправил дарителю обновленный вишлист",
    text2="обновил(а) свой вишлист:"
)
create_wish_list = Feature(
    activators=["создать новый вишлист"],
    button="Создать вишлист",
    text="Напишите мне новый вишлист. Старый при этом будет перезаписан.",
    text2="Готово, записал новый вишлист. Сейчас он выглядит так:",
    descr="Создать новый вишлист.",
    state_key="create_wish_list",
)
append_wish_list = Feature(
    activators=["дополнить текущий вишлист"],
    button="Дополнить вишлист",
    text="Напишите мне, что бы вы хотели добавить к вашему текущему вишлисту.",
    text2="Готово, дополнил текущий вишлист. Сейчас он выглядит так:",
    descr="Дополнить текущий вишлист.",
    state_key="append_wish_list",
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
    prefix="join",
    descr="В вашу комнату зашел новый участник: {0}"
)
user_leave_approve = Feature(
    text="Вы точно хотите выйти из комнаты?"
)
user_leave = Feature(
    text="Вы вышли из комнаты, теперь можете создать свою или присоединиться к созданной по ссылке.",
    text2="Из вашей комнаты вышел участник: {0}",
    button="Выйти из комнаты",
    descr="Выйти из комнаты",
    state_key="user_leave",
)
kick_user_not_found = Feature(
    text="Не могу найти в вашей комнате этого участника. Используйте кнопки, пожалуйста."
)
kick_user = Feature(
    text="Пользователь {0} был выгнан из комнаты",
    text2="Вы уверены что хотите выгнать пользователя {0} из комнаты?",
    button="Выгнать",
    descr="Выгнать пользователя из комнаты",
    prefix="выгнать",
    state_key="user_kick",
)
start_shuffle = Feature(
    text="найдет ваш подарок под ёлкой",
    button="Провести жеребьевку",
    descr="Провести жеребьевку",
    text2="Кстати, его(ее) вишлист:",
)
check_shuffle = Feature(
    text="Начинаю шафл, проверяю готовность всех участников.",
    text2="заблокировал бота, не могу провести жеребьевку. Нужно выгнать этого участника из комнаты (либо попросить "
          "его разблокировать бота, если он сделал это случайно) и уже после этого провести жеребьевку.",
)
reshuffle = Feature(
    button="Перебросить жребий",
    descr="Провести жеребьевку заново (вдруг кто-то очень недоволен или что-то пошло не так)"
)
check_room = Feature(
    text="Сейчас в вашей комнате эти люди",
    button="Участники",
    descr="Посмотреть список всех друзей в комнате. Если кто-то из них вам больше не друг, его можно выгнать"
)
delete_room = Feature(
    text="Комната удалена насовсем",
    text2="Вы уверены что хотите удалить комнату насовсем?",
    button="Удалить комнату",
    button_color="red",
    descr="Удалить комнату насовсем",
    state_key="room_delete",
)
room_error = Feature(
    text="Такой комнаты не существует, попробуйте еще раз",
    text2="Вы уже в комнате, вам не нужно переходить по ссылке или скидывать мне код",
)
sucseed_shuffle = Feature(
    text="Жеребьевка прошла успешно!"
)
access_error = Feature(
    text="Доступ ограничен: Вы не админ комнаты"
)
kicked_user = Feature(
    text="Увы и ах, но вас, к сожалению, выгнали из комнаты {admin_name}"
)
pls_sub = Feature(
    text="Если вам понравился наш бот, не забывайте подписываться на него, чтобы не пропускать новые крутые фичи!"
)
wrong_command = Feature(
    text="Я простой бот и понимаю только определенные команды. Правила игры в тайного санту и помощь с ботом по "
         "команде «помощь» или кнопке ниже."
)
rules_and_help = Feature(
    activators=["help", "помощь", "rules", "правила"],
    button="Помощь",
    text="Содержание:\n1. Как зайти в комнату\n2. Как написать вишлист\n3. Когда я получу имя, кому дарить\n4. Как "
         "работает бот\n5. Общие правила игры в тайного санту.\n\n1) Чтобы зайти в чью-то уже созданную комнату вам "
         f"нужно отправить в этот диалог специальный код, который начинается с «{user_adding.prefix}» и далее идут "
         f"цифры, например «{user_adding.prefix}12345». Этот код вы должны получить от вашего организатора.\n\n"
         f"2) Для управления вишлистом нужно нажать на кнопку вишлиста"
         f" в главном меню, или написать боту «{wish_list_menu.button}». После этого вы попадете в меню вишлиста, где "
         "можно создать/перезаписать или дополнить вишлист. Нажмите нужную вам кнопку и следующим сообщением напишите "
         "боту то, что бы вы хотели получить в подарок от тайного санты. Если в вашей комнате уже провели жеребьевку,"
         " бот отправит обновленный вишлист вашему дарителю.\n\n3) Вы получите имя того, кому вам дарить подарок после"
         " того, как админ вашей комнаты проведет жеребьевку. Админ организует для вас и ваших друзей игру в тайного "
         "санту, скидывает код для захода в комнату и проводит жеребьевку.\n\n4) Как работает бот? Начинается с того, "
         "что организатор должен создать комнату внутри бота и пригласить туда с помощью специального кода всех, кого"
         " он хочет. После того как все участники зашли в комнату и написали свои вишлисты админ проводит жеребьевку. "
         "Жеребьевка проводится так: бот собирает всех участников комнаты в некий «хоровод», расставляя в нем "
         "участников в случайном порядке, и получается так, что тот кто слева дарит тому кто справа, и так по кругу,"
         " пока  он не замкнется. Процесс жеребьевки полностью автоматический и в него не может вмешаться ни админ, ни"
         " даже создатель бота. Если вы вдруг остались недовольны результатами жеребьевки, можно попросить вашего "
         "админа провести ее заново.\n\n5. Общие правила игры в тайного санту: это новогодняя (и не только) игра, в"
         "которой коллеги, друзья или родственники анонимно обмениваются подарками. Данный бот призван помочь вам "
         "в организации этой замечательной игры!\n\nЕсли остались вопросы можно написать создателю бота: {0}",
)
