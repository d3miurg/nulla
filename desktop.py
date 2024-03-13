from PyQt6 import QtWidgets
from PyQt6 import QtCore
import core
import os

app = QtWidgets.QApplication([])

main_window = QtWidgets.QMainWindow()
screen_size = app.screens()[0].availableGeometry()
main_window.setGeometry(int(screen_size.width() / 4),
                        int(screen_size.height() / 4),
                        int(screen_size.width() / 2),
                        int(screen_size.height() / 2))
main_window.setFixedSize(main_window.width(), main_window.height())
main_window.setWindowTitle('Nulla Client')
main_window.hide()

login_form = QtWidgets.QWidget(main_window)
login_input = QtWidgets.QLineEdit(login_form)
password_input = QtWidgets.QLineEdit(login_form)
accept_button = QtWidgets.QPushButton('Войти', login_form)
layout = QtWidgets.QVBoxLayout(login_form)
layout.addWidget(login_input)
layout.addWidget(password_input)
layout.addWidget(accept_button)
login_form.setLayout(layout)
login_form.setGeometry(int(main_window.width() / 3),
                       0,
                       int(main_window.width() / 3),
                       int(main_window.height()))

communities_container = QtWidgets.QListWidget(main_window)
communities = {}
communities_container.setGeometry(0,
                                  0,
                                  int(main_window.width() / 3),
                                  int(main_window.height()))
communities_container.hide()

chats_container = QtWidgets.QListWidget(main_window)
chats = {}
chat_id = 1
chats_container.setGeometry(int(main_window.width() / 3),
                            0,
                            int(main_window.width() / 3),
                            int(main_window.height()))
chats_container.hide()

messages_container = QtWidgets.QWidget(main_window)
last_message = []
messages_list = QtWidgets.QListWidget(messages_container)
input_field = QtWidgets.QTextEdit(messages_container)
send_button = QtWidgets.QPushButton('Отправить', messages_container)
layout = QtWidgets.QVBoxLayout(messages_container)
layout.addWidget(messages_list)
layout.addWidget(input_field)
layout.addWidget(send_button)
messages_container.setLayout(layout)
messages_container.setGeometry(int(main_window.width() / 3),
                               0,
                               int(main_window.width() * 2 / 3),
                               int(main_window.height()))
messages_container.hide()


class Updater(QtCore.QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        global last_message
        global messages_list
        while True:
            current_message = core.get_messages(chat_id, 1)
            if current_message != last_message:
                messages_list.addItem(current_message[0][0])
                messages_list.scrollToBottom()
                last_message = current_message


def login():
    global communities
    email = login_input.text()
    password = password_input.text()
    status = core.login(email, password)

    if status == '200':
        login_form.hide()
        communities = core.get_communities()
        communities_container.addItems(communities.keys())
        communities_container.show()

    else:
        print(status)


def enter_community():
    global chats
    messages_container.hide()
    community_name = communities_container.selectedItems()[0].text()
    community_id = communities[community_name]
    chats = core.enter_community(community_id)
    chats_container.clear()
    chats_container.addItems(chats.keys())
    chats_container.show()


def enter_chat():
    global last_message
    global chat_id
    global chats

    chat_name = chats_container.selectedItems()[0].text()
    chat_id = chats[chat_name]

    updater = Updater()
    updater.start()

    messages_list.clear()
    last_messages = core.get_messages(chat_id, 25)
    [messages_list.addItem(n[0]) for n in last_messages]
    messages_list.scrollToBottom()
    chats_container.hide()
    messages_container.show()


accept_button.clicked.connect(login)
communities_container.itemClicked.connect(enter_community)
chats_container.itemClicked.connect(enter_chat)

if __name__ == '__main__':
    main_window.show()
    app.exec()

    core.logout()
    os._exit(0)
