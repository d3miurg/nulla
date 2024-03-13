from PyQt6 import QtWidgets
import core
import os

app = QtWidgets.QApplication([])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        screen_size = app.screens()[0].availableGeometry()
        self.setGeometry(int(screen_size.width() / 4),
                         int(screen_size.height() / 4),
                         int(screen_size.width() / 2),
                         int(screen_size.height() / 2))
        self.setWindowTitle('Nulla Client')


class LoginForm(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        login_input = QtWidgets.QLineEdit(self)
        password_input = QtWidgets.QLineEdit(self)
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(login_input, 0, 1, 0, 1)
        layout.addWidget(password_input, 1, 1, 2, 2)
        self.setLayout(layout)


'''
login_container = QtWidgets.QWidget(window)
login_container.setGeometry(0,
                            0,
                            window.size().width(),
                            window.size().height())
login_container.setGeometry
layout = QtWidgets.QGridLayout(login_container)

login_label = gui.SelfShowingLineEdit(layout, 0, 0, login_container)
login_label.show()'''


if __name__ == '__main__':
    main_window = MainWindow()
    login_form = LoginForm(main_window)
    main_window.show()
    app.exec()

    print('Выход (закрытие окна)')
    core.logout()
    os._exit(0)
