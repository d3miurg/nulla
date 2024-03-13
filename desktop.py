from PyQt6 import QtWidgets
import core
import os
import threading

app = QtWidgets.QApplication([])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        screen_size = app.screens()[0].availableGeometry()
        self.setGeometry(int(screen_size.width() / 4),
                         int(screen_size.height() / 4),
                         int(screen_size.width() / 2),
                         int(screen_size.height() / 2))
        self.setFixedSize(self.width(), self.height())

        self.setWindowTitle('Nulla Client')


class ChatContainer(QtWidgets.QWidget):
    def __init__(self, parent, chat_id):
        super().__init__(parent)
        self.parent = parent
        self.last = []
        self.chat_id = chat_id

        self.messages_list = QtWidgets.QListWidget(self)
        input_field = QtWidgets.QTextEdit(self)
        send_button = QtWidgets.QPushButton('Отправить', self)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.messages_list)
        layout.addWidget(input_field)
        layout.addWidget(send_button)
        self.setLayout(layout)

        self.setGeometry(int(parent.width() / 3),
                         0,
                         int(parent.width() * 2 / 3),
                         int(parent.height()))

        chat_thread = threading.Thread(target=self.get_message)
        chat_thread.start()

    def get_message(self):
        while True:
            last_message = core.get_messages(self.chat_id, 1)
            if last_message != self.last:
                self.messages_list.addItem(last_message[0])
                self.last = last_message


class ChatsList(QtWidgets.QListWidget):
    def __init__(self, parent, chats):
        super().__init__(parent)
        self.parent = parent
        self.chats = chats

        self.setGeometry(int(parent.width() / 3),
                         0,
                         int(parent.width() / 3),
                         int(parent.height()))

        self.itemClicked.connect(self.enter_chat)

    def update(self, chats):
        self.clear()
        self.addItems(chats.keys())
        self.chats = chats

    def enter_chat(self):
        selected_chat = self.selectedItems()[0].text()
        chat_id = self.chats[selected_chat]
        chat = ChatContainer(self.parent, chat_id)
        chat.show()
        self.hide()


class CommunitiesList(QtWidgets.QListWidget):
    def __init__(self, parent, communities):
        super().__init__(parent)
        self.parent = parent
        self.communities = communities

        self.chats_list = ChatsList(self.parent, [])
        self.chats_list.hide()

        self.addItems(list(communities.keys()))

        self.itemClicked.connect(self.enter_community)

        self.setGeometry(0,
                         0,
                         int(parent.width() / 3),
                         int(parent.height()))

    def enter_community(self):
        community_name = self.selectedItems()[0].text()
        community_id = self.communities[community_name]
        chats = core.enter_community(community_id)
        self.chats_list.update(chats)
        self.chats_list.show()


class LoginForm(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        login_input = QtWidgets.QLineEdit(self)
        password_input = QtWidgets.QLineEdit(self)
        accept_button = QtWidgets.QPushButton('Войти', self)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(login_input, 0, 0)
        layout.addWidget(password_input, 1, 0)
        layout.addWidget(accept_button, 3, 0)
        self.setLayout(layout)

        self.setGeometry(int(parent.width() / 3),
                         0,
                         int(parent.width() / 3),
                         int(parent.height()))

        accept_button.pressed.connect(lambda: self.login(login_input,
                                                         password_input))

    def login(self, login_input, password_input):
        status = core.login(login_input.text(), password_input.text())
        if status == '200':
            communities = core.get_communities()
            communities_list = CommunitiesList(self.parent, communities)
            communities_list.show()
            self.hide()
        else:
            print(status)


if __name__ == '__main__':
    main_window = MainWindow()
    login_form = LoginForm(main_window)

    main_window.show()
    app.exec()

    core.logout()
    os._exit(0)
