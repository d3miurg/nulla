import tkinter
from functools import partial

print('Соединение с Амино')
import core

print('Загрузка окна')

def enter_chat(chat_id, buttons):
    last_messages = core.get_messages(chat_id)
    print(last_messages)

def enter_community(com_id, buttons):
    chats = core.enter_community(com_id)

    for button in buttons:
        button.place_forget()

    chat_buttons = []

    for chat in chats:
            chat_buttons.append(tkinter.Button(text = chat[0], command = partial(enter_chat, chat[1], buttons)))

    i = .1

    print(chat_buttons)

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
            buttons.append(tkinter.Button(text = community[0], command = partial(enter_community, community[1], buttons)))

        i = .1

        for button in buttons:
            button.place(relx = .1, rely = i)
            i += .1
    
root = tkinter.Tk()

root.title('Nulla Client')
root.geometry('500x500+100+100')

login_var = tkinter.StringVar()
password_var = tkinter.StringVar()
error_var = tkinter.StringVar()

login_page_list = []

login_label = tkinter.Label(text = 'Логин')
login_page_list.append(login_label)
login_entry = tkinter.Entry(textvariable = login_var)
login_page_list.append(login_entry)
password_label = tkinter.Label(text = 'Пароль')
login_page_list.append(password_label)
password_entry = tkinter.Entry(textvariable = password_var, show = '*')
login_page_list.append(password_entry)
accept_button = tkinter.Button(text = 'Войти', command = partial(login, login_var, password_var, error_var, login_page_list))
login_page_list.append(accept_button)
error_label = tkinter.Label(textvariable = error_var, fg = 'red')
login_page_list.append(error_label)

login_label.place(relx=.1, rely=.1)
login_entry.place(relx=.1, rely=.2)
password_label.place(relx=.1, rely=.3)
password_entry.place(relx=.1, rely=.4)
accept_button.place(relx=.1, rely=.6)
error_label.place(relx=.1, rely=.5)

root.mainloop()

print('Выход (закрытие окна)')
