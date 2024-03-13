import aminofix as amino
import queue
import os
import json
import requests


message_queue = queue.Queue()

safe_messages = []

user = amino.Client()
sub_user = None


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
def login(email, password):

    try:
        user.login(email, password)
        return '200'

    except amino.lib.util.exceptions.InvalidEmail:
        return 'Аккаунт не найден'

    except amino.lib.util.exceptions.AccountDoesntExist:
        return 'Аккаунт не найден'

    except amino.lib.util.exceptions.InvalidAccountOrPassword:
        return 'Неверный пароль'

    except amino.lib.util.exceptions.InvalidPassword:
        return 'Неверный пароль'


@handle_errors
def get_communities():
    communities = {}
    comms = user.sub_clients()

    for i in range(0, len(comms.name)):
        communities[comms.name[i]] = comms.comId[i]

    return communities


@handle_errors
def enter_community(com_id):
    global sub_user
    sub_user = amino.SubClient(comId=com_id, profile=user.profile)
    chats = sub_user.get_chat_threads()

    ret_chats = {}

    for i in range(0, len(chats.title)):
        if chats.title[i] is None:
            ret_chats['Безымянный чач ' + str(i)] = chats.chatId[i]

        else:
            ret_chats[chats.title[i]] = chats.chatId[i]

    return ret_chats


@handle_errors
def get_messages(chat_id, count):
    non_text = 'НЕ ТЕКСТОВОЕ СООБЩЕНИЕ ТИПА '

    new_messages = sub_user.get_chat_messages(chat_id, count)

    '''if count != len(new_messages.content):
        count = len(new_messages.content) - 1'''

    current_iteration = []

    for t in range(len(new_messages.content)):
        first_part = new_messages.author.nickname[t] + ': '

        if new_messages.content[t] is None:
            full_message = first_part + non_text + str(new_messages.type[t])

        else:
            full_message = first_part + new_messages.content[t]

        current_iteration.append([full_message,
                                  new_messages.author.userId[t],
                                  new_messages.messageId[t],
                                  new_messages.type[t]])

    current_iteration.reverse()

    return current_iteration


@handle_errors
def return_message(chat_id):

    repr_file = open('chat_repr.txt', 'w', encoding='utf-8')

    while True:
        if not message_queue.empty():
            message = message_queue.get()
            repr_file.write(message + '\n')
            yield message

        else:
            yield None


@handle_errors
def send_message(chat_id, message=None, tk_var=None, tk_error=None):
    try:
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
def push_read(chat_id):
    sub_user.edit_chat(chat_id, viewOnly=True)


@handle_errors
def push_write(chat_id):
    sub_user.edit_chat(chat_id, viewOnly=False)


@handle_errors
def logout():
    user.logout()
