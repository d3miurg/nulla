print('Это тестовая версия. Я буду только рад, если ты её сломаешь. Главное, расскажи мне, как ты это сделал')
print('Я не хочу лишний раз ломать терминал, так что придётся работать по максимально ебанутой схеме. Всё поменяется, когда появится графика')
print('Настройка')

import sys
import json

try:
    try:
        import amino
        import getpass
        import warnings

    except ImportError:
        answer = input('Нужные библиотеки не найдены. Возможно, вы запускаете приложение в первый раз. Хотите произвести настройку? [y/n]')

        valid_answers = ['y', 'yes', 'д', 'да']
        help_answers = ['h', 'help']

        if answer in valid_answers:
            print('Ожидайте')

            import firstrunsetup as frs
            frs.start()

        elif answer in help_answers:
            print('Если вы согласитесь, приложение установит библиотеку для работы с Амино и фиксы для неё')
            answer = input()

            if answer in valid_answers:
                print('Ожидайте')

                import firstrunsetup as frs
                frs.start()

            else:
                print('Выход')
                sys.exit()

        else:
            print('Выход')
        sys.exit()

    tab_str = '    '

    print('Соединение с Амино')
    user = amino.Client()

    logged = False
    while not logged:
        try:
            with warnings.catch_warnings(record = True) as w:
                login = input(tab_str + 'Логин: ')
                password = getpass.getpass(prompt = tab_str + 'Пароль: ')
                user.login(login, password)
                logged = True

        except amino.lib.util.exceptions.InvalidEmail:
            print('Аккаунт не найден')

        except amino.lib.util.exceptions.InvalidAccountOrPassword:
            print('Неверный пароль')

        except amino.lib.util.exceptions.InvalidPassword:
            print('Неверный пароль')

    print('Получение списка сообществ')
    comms = user.sub_clients()
    print('Выберите сообщество:')
    i = 0
    for name in comms.name:
        print(tab_str + str(i) + '. ' + name)
        i += 1

    number = int(input())

    print('Вход в сообщество')
    sub_user = amino.SubClient(comId = comms.comId[number], profile = user.profile)
    print('Получение чатов')
    chats = sub_user.get_chat_threads()
    print('Выберите чат:')
    i = 0
    for title in chats.title:
        if title is None:
            title = 'Безымянный чач'
        print(tab_str + str(i) + '. ' + title)
        i += 1

    number = int(input())

    chat_id = chats.chatId[number]

    print('Сколько сообщений загрузить?')
    print('Отсчёт идёт снизу вверх')
    number = int(input())

    last_messages = sub_user.get_chat_messages(chat_id, number)

    lst = []

    for t in range(0, number, 1):
        print('хуй пизда сковорода')
        first_part = last_messages.author.nickname[t] + ': '

        if last_messages.content[t] is None:
            full_message = first_part + 'НЕ ТЕКСТОВОЕ СООБЩЕНИЕ ТИПА ' + str(last_messages.type[t])

        else:
            full_message = first_part + last_messages.content[t]

        lst.append(full_message + '\n')

    lst.reverse()

    for o in lst:
        print(o)

    main_flag = True

    nick = sub_user.profile.nickname
    last_msg = last_messages.content[0]
    
    while main_flag:
        print('0. Обновить')
        print('1. Отправить сообщение')
        stat = int(input())

        if stat == 0:
            last_messages = sub_user.get_chat_messages(chat_id, 1)
            if last_messages.content[0] != last_msg:
                first_part = last_messages.author.nickname[0] + ': '

                if last_messages.content[0] is None:
                    full_message = first_part + 'НЕ ТЕКСТОВОЕ СООБЩЕНИЕ ТИПА ' + str(last_messages.type[0])

                else:
                    full_message = first_part + last_messages.content[0]

                print(full_message + '\n')
                last_msg = last_messages.content[0]

            else:
                print('Новых сообщений нет')

        elif stat == 1:
            new_message = input('Текст: ')

            print('Отправка')
            sub_user.send_message(chat_id, new_message)

            print('Отправлено')

    user.logout()
    

except json.decoder.JSONDecodeError:
    print('Сервера упали. Как всегда, блять')
    sys.exit()

