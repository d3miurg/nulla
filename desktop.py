from PyQt6 import QtWidgets
from nullaLowLevel import core
import os

import gui

def update_chat(chat_id, chat_list, message_generator):
    global last_messages

    message = next(message_generator)

    if not (message is None):
        chat_list.insert(tkinter.END, message)

    root.after(150, update_chat, chat_id, chat_list, message_generator)

def enter_chat(chat_id, buttons):
    message_var = tkinter.StringVar()
    chat_error_var = tkinter.StringVar()

    chat_container = tkinter.LabelFrame(root)
    chat_scroll = tkinter.Scrollbar(chat_container)
    chat_list = tkinter.Listbox(chat_container, yscrollcommand = chat_scroll.set)
    chat_scroll.config(command = chat_list.yview)

    message_entry = tkinter.Entry(textvariable = message_var)
    send_button = tkinter.Button(text = 'Отправить', command = functools.partial(core.send_message, chat_id, tk_var = message_var, tk_error = chat_error_var))
    chat_error_label = tkinter.Label(textvariable = chat_error_var)

    view_button = tkinter.Button(text = 'Только чтение', command = functools.partial(core.push_read, chat_id))

    chat_container.place(relx = .05, rely = .05, relheight = .6, relwidth = .9)
    chat_list.place(relx = 0, rely = 0, relheight = 1, relwidth = .95)
    chat_scroll.place(relx = .95, rely = 0, relheight = 1)
    message_entry.place(relx = .05, rely = .7)
    send_button.place(relx = .05, rely = .8)
    view_button.place(relx = .5, rely = .7)

    for button in buttons:
        button.place_forget()

    message_generator = core.return_message(chat_id)

    root.after(150, update_chat, chat_id, chat_list, message_generator)

def enter_community(com_id, buttons):
    chats = core.enter_community(com_id)

    for button in buttons:
        button.place_forget()

    chat_buttons = []

    for chat in chats:
        chat_buttons.append(tkinter.Button(text = chat[0], command = functools.partial(enter_chat, chat[1], chat_buttons)))

    i = .1

    for button in chat_buttons:
        button.place(relx = .1, rely = i)
        i += .1

def login(email, password, error, page_elements):
    status = core.login(email.get(), password.get())

    if status != 200:
        error.set(status)

    else:
        communities = core.get_communities()

        for element in page_elements:
            element.place_forget()

        buttons = []

        for community in communities:
            buttons.append(tkinter.Button(text = community[0], command = functools.partial(enter_community, community[1], buttons)))

        i = .1

        for button in buttons:
            button.place(relx = .1, rely = i)
            i += .1


app = QtWidgets.QApplication([])
screen_size = app.screens()[0].availableGeometry()
window = QtWidgets.QMainWindow()
window.setGeometry(int(screen_size.width() / 4),
                   int(screen_size.height() / 4),
                   int(screen_size.width() / 2),
                   int(screen_size.height() / 2))
window.setWindowTitle('Nulla Client')

login_container = QtWidgets.QWidget(window)
login_container.setGeometry(0,
                            0,
                            window.size().width(),
                            window.size().height())
login_container.setGeometry
layout = QtWidgets.QGridLayout(login_container)

login_label = gui.SelfShowingLineEdit(layout, 0, 0, login_container)
login_label.show()

'''login_label = QtWidgets.QLabel('Логин:', login_container)
login_input = QtWidgets.QLineEdit(login_container)
password_label = None
password_input = QtWidgets.QLineEdit(login_container)
password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
error_out = QtWidgets.QLabel(login_container)

layout.addWidget(login_label, 0, 0)
layout.addWidget(login_input, 1, 0)
layout.addWidget(password_input, 2, 0)
layout.addWidget(error_out, 3, 0)

login_container.show()
login_input.show()
password_input.show()
error_out.show()'''

if __name__ == '__main__':
    print('Подключение к Амино')
    core.start()
    print('Подключено')
    window.show()
    app.exec()

    print('Выход (закрытие окна)')
    os._exit(core.stop())

'''

login_page_list = []

login_label = tkinter.Label(text = 'Логин')
login_page_list.append(login_label)
login_entry = tkinter.Entry(textvariable = login_var)
login_page_list.append(login_entry)
password_label = tkinter.Label(text = 'Пароль')
login_page_list.append(password_label)
password_entry = tkinter.Entry(textvariable = password_var, show = '*')
login_page_list.append(password_entry)
accept_button = tkinter.Button(text = 'Войти', command = functools.partial(login, login_var, password_var, error_var, login_page_list))
login_page_list.append(accept_button)
error_label = tkinter.Label(textvariable = error_var, fg = 'red')
login_page_list.append(error_label)

login_label.place(relx=.1, rely=.1)
login_entry.place(relx=.1, rely=.2)
password_label.place(relx=.1, rely=.3)
password_entry.place(relx=.1, rely=.4)
accept_button.place(relx=.1, rely=.6)
error_label.place(relx=.1, rely=.5)'''