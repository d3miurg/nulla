#для начала, реализуй чаты, сообщества и посты
#все форы переписать
#вынести универсальные классы в отдельный файл
#но это когда появится комп
import tkinter
import functools
import queue

import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

global core

app = QApplication(sys.argv)
mainWindow = QWidget()

def updateScreen(*elements):
    for n in mainWindow.children():
        print(n)
        n.hide()
        
    for n in elements:
        print(n)
        n.show()

#все эти классы-потоки нужно объединить в один
#сделав QThread более похожим на threading.Thread
#и добавть к ним сигналы
#повесить на один поток всю работу с сервером
class chatFormer(QThread):
    def __init__(self, communityId):
        super().__init__()
        self.communityId = communityId
    
    def run(self):
        print('chat')
        
class logger(QThread):
    global backBuffer
    
    def __init__(self, login, password):
        super().__init__()
        self.login = login
        self.password = password
    
    def run(self):
        print('enter thread')
        core.login(self.login, self.password)
        communities = core.get_communities()
        print('process')
        
        yOffset = 50
        buttons =[]
        for community in communities:
            print('cycle')
            self.chatThread = chatFormer(community[1])
            communityButton = QPushButton(community[0],mainWindow)
            communityButton.clicked.connect(self.chatThread.start)
            communityButton.resize(50, 150)
            communityButton.move(50, yOffset)
            buttons.append(communityButton)
            yOffset += 50
        
        print('end')
        updateScreen(*buttons)
        print('swap')

class coreConnector(QThread):
    def __init__(self):
        super().__init__()
    
    def run(self):
        global core
        
        from nullaLowLevel import core
        core.start()
        
        loginForm = loginFormer(mainWindow)
        updateScreen(loginForm)

#тут начинаются классы форм
#возможно, он не нужен
class loginFormer(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.loginField = QLineEdit(self)
        self.loginField.resize(350, 50)
        self.loginField.move(50, 50)

        self.passwordField = QLineEdit(self)
        self.passwordField.setEchoMode(QLineEdit.Password)
        self.passwordField.resize(350, 50)
        self.passwordField.move(50, 120)
        
        self.loginButton = QPushButton('Войти', self)
        self.loginButton.clicked.connect(self.login)
        self.loginButton.resize(self.loginButton.sizeHint())
        self.loginButton.move(50, 190)
    
    def login(self):
        self.loginAction = logger(self.loginField.text(), self.passwordField.text())
        
        self.statusLabel = QLabel(self)
        self.statusLabel.setText('Вход в аккаунт')
        self.statusLabel.resize(self.statusLabel.sizeHint())
        self.statusLabel.move(50, 260)
        self.statusLabel.show()
        
        self.loginAction.start()
    
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

    chat_container.place(relx = .05, rely = .05, relheight = .6, relwidth = .9)
    chat_list.place(relx = 0, rely = 0, relheight = 1, relwidth = .95)
    chat_scroll.place(relx = .95, rely = 0, relheight = 1)
    message_entry.place(relx = .05, rely = .7)
    send_button.place(relx = .05, rely = .8)

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

#для компа
#root.title('Nulla Client')
#root.geometry('500x500+100+100')

if __name__ == '__main__':
    mainWindow.show()
    loadLabel = QLabel(mainWindow)
    loadLabel.setText('Соединение с Амино')
    loadLabel.resize(350, 50)
    loadLabel.move(50, 50)
    loadLabel.show()

    connectionThread = coreConnector()
    connectionThread.start()
    
    app.exec()
    
    core.stop()
    
sys.exit()