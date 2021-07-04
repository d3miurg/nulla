import sys
import json
import base64
import string
import random
import requests
from hashlib import sha1

try:
    try:
        import amino

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
                print('Выход (нет нужных библиотек)')
                sys.exit()

        else:
            print('Выход (нет нужных библиотек)')
            sys.exit()

    except json.decoder.JSONDecodeError:
        print('Сервера упали. Как всегда, блять')
        sys.exit()

    except requests.exceptions.SSLError:
        print('А де интернет?')
        sys.exit()

    user = amino.Client()

except json.decoder.JSONDecodeError:
    print('Сервера упали. Как всегда, блять')
    sys.exit()

def login(email, password):
    try:
        try:
            user.login(email, password)

            return 200

        except amino.lib.util.exceptions.InvalidEmail:
            return 'Аккаунт не найден'

        except amino.lib.util.exceptions.AccountDoesntExist:
            return 'Аккаунт не найден'

        except amino.lib.util.exceptions.InvalidAccountOrPassword:
            return 'Неверный пароль'

        except amino.lib.util.exceptions.InvalidPassword:
            return 'Неверный пароль'

        except amino.lib.util.exceptions.ActionNotAllowed:
            login_info = open('device.json', 'r')
            info = json.load(login_info)
            login_info.close()

            origin_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 69))
            new_id = '01' + (MetaSpecial := sha1(origin_string.encode("utf-8"))).hexdigest() + sha1(bytes.fromhex('01') + MetaSpecial.digest() + base64.b64decode("6a8tf0Meh6T4x7b0XvwEt+Xw6k8=")).hexdigest()
            info['device-id'] = new_id

            login_info = open('device.json', 'w')
            json.dump(info, login_info)
            login_info.close()
            
            return 'Амино обнаружило, что вы используете кастомный клиент. Мы уже подделали для вас паспорт, попробуйте войти ещё раз'

    except json.decoder.JSONDecodeError:
        print('Сервера упали. Как всегда, блять')
        sys.exit()

    except requests.exceptions.SSLError:
        print('А де интернет?')
        sys.exit()

def get_communities():
    try:
        communities = []
        comms = user.sub_clients()

        for i in range(0, len(comms.name)):
            communities.append([comms.name[i], comms.comId[i]])

        return communities

    except json.decoder.JSONDecodeError:
        print('Сервера упали. Как всегда, блять')
        sys.exit()

def enter_community(com_id):
    try:
        global sub_user
        sub_user = amino.SubClient(comId = com_id, profile = user.profile)
        chats = sub_user.get_chat_threads()

        ret_chats = []

        for i in range(0, len(chats.title)):
            if chats.title[i] is None:
                ret_chats.append(['Безымянный чач', chats.chatId[i]])

            else:
                ret_chats.append([chats.title[i], chats.chatId[i]])

        return ret_chats

    except json.decoder.JSONDecodeError:
        print('Сервера упали. Как всегда, блять')
        sys.exit()

    except requests.exceptions.SSLError:
        print('А де интернет?')
        sys.exit()

def get_last_messages(chat_id, count = 25, update = False):
    try:
        global sub_user
        last_messages = sub_user.get_chat_messages(chat_id, count)

        lst = []

        for t in range(count):
            first_part = last_messages.author.nickname[t] + ': '

            if last_messages.content[t] is None:
                full_message = first_part + 'НЕ ТЕКСТОВОЕ СООБЩЕНИЕ ТИПА ' + str(last_messages.type[t])

            else:
                full_message = first_part + last_messages.content[t]

            lst.append(full_message)

        if not update:
            global last_msg
            last_msg = lst[0]

        lst.reverse()
        return lst

    except json.decoder.JSONDecodeError:
        print('Сервера упали. Как всегда, блять')
        sys.exit()

    except requests.exceptions.SSLError:
        print('А де интернет?')
        sys.exit()

def get_new_messages(chat_id, queue):
    try:
        global last_msg
        while True:
            last_messages = get_last_messages(chat_id, 10, True)

            index = last_messages.index(last_msg)

            lst = []

            if index != 9:
                for n in range(index + 1, 10):
                    lst.append(last_messages[n])

                last_msg = lst[len(lst) - 1]

            for message in lst:
                queue.put(message)

    except json.decoder.JSONDecodeError:
        print('Сервера упали. Как всегда, блять')
        sys.exit()

    except requests.exceptions.SSLError:
        print('А де интернет?')
        sys.exit()

def send_message(chat_id, message):
    try:
        global sub_user
        sub_user.send_message(chat_id, message.get())
        message.set('')

    except json.decoder.JSONDecodeError:
        print('Сервера упали. Как всегда, блять')
        sys.exit()

    except requests.exceptions.SSLError:
        print('А де интернет?')
        sys.exit()

def stop():
    try:
        user.logout()

    except json.decoder.JSONDecodeError:
        print('Сервера упали. Как всегда, блять')
        sys.exit()

    except requests.exceptions.SSLError:
        print('А де интернет?')
        sys.exit()
