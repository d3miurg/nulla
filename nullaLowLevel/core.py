import sys
import threading
import queue
import os
import nullaLowLevel.protection.lumus as lumus

import base64
import string
import random
from hashlib import sha1

import json
import requests

message_queue = queue.Queue()

tk_root = None

def handle_errors(func):
    def exec_func(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res

        except json.decoder.JSONDecodeError:
            print('Сервера упали. Как всегда, блять')
            os.abort()

        except requests.exceptions.SSLError:
            print('А де интернет?')
            os.abort()

    return exec_func

@handle_errors
def start():
    global amino
    global user

    try:
        import amino

    except ImportError:
        answer = input('Нужные библиотеки не найдены. Возможно, вы запускаете приложение в первый раз. Хотите произвести настройку? [y/n]')

        valid_answers = ['y', 'yes', 'д', 'да']
        help_answers = ['h', 'help', 'п', 'помощь']

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
    
    user = amino.Client()

@handle_errors
def compare(message1, message2):
    compare_index = 0
    lenght_index = 0
    
    if len(message1) > len(message2):
        short_message = message2
        long_message = message1

    else:
        short_message = message1
        long_message = message2

    for i in short_message:
        if i == long_message[lenght_index]:
            compare_index += 1

        lenght_index += 1

    ratio = (compare_index * 100) / lenght_index

    return ratio

@handle_errors
def login(email, password):
    global user

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

    '''except:
        return 'Неизвестная ошибка'''

@handle_errors
def get_communities():
    communities = []
    comms = user.sub_clients()

    for i in range(0, len(comms.name)):
        communities.append([comms.name[i], comms.comId[i]])

    return communities

@handle_errors
def enter_community(com_id):
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

@handle_errors
def get_messages(chat_id, count, last = []):
    global sub_user

    new_messages = sub_user.get_chat_messages(chat_id, count)

    if count != len(new_messages.content):
            count = len(new_messages.content) - 1

    current_iteration = []

    for t in range(count):
        first_part = new_messages.author.nickname[t] + ': '

        if new_messages.content[t] is None:
            full_message = first_part + 'НЕ ТЕКСТОВОЕ СООБЩЕНИЕ ТИПА ' + str(new_messages.type[t])

        else:
            full_message = first_part + new_messages.content[t]

        current_iteration.append([full_message, new_messages.author.userId[t], new_messages.messageId[t], new_messages.type[t]])

    current_iteration.reverse()

    for message in current_iteration:
        if not (message in last):
            message_queue.put(message[0])

    return current_iteration

@handle_errors
def check_messages(chat_id):
    last_iteration = get_messages(chat_id, 25)

    while threading.main_thread().is_alive():
        current_iteration = get_messages(chat_id, 4, last_iteration)

        items = len(current_iteration) - 1

        lumus.spam_check(current_iteration, items + 1, chat_id, sub_user)
            
        last_iteration = current_iteration

@handle_errors
def return_message(chat_id):
    listner = threading.Thread(target = check_messages, args = [chat_id])
    listner.start()
        
    while True:
        if not message_queue.empty():
            yield message_queue.get()

        else:
            yield None

@handle_errors
def send_message(chat_id, message = None, tk_var = None, tk_error = None):
    try:
        global sub_user
        send_ready = ''
        if tk_var:
            send_ready = tk_var.get()
            tk_var.set('')

        elif message:
            send_ready = message

        else:
            if tk_error:
                tk_error.set('Нельзя отправить пустое сообщение')

            else:
                return 'Нельзя отправить пустое сообщение'

        sub_user.send_message(chat_id, send_ready)

    except amino.lib.util.exceptions.ChatViewOnly:
        if tk_error:
            tk_error.set('В чате установлен режим чтения')

        else:
            return 'В чате установлен режим чтения'

@handle_errors
def stop():
    user.logout()