from PyQt6 import QtWidgets


class SelfShowingWidget(QtWidgets.QWidget):
    def __init__(self,
                 grid: QtWidgets.QGridLayout,
                 row: int,
                 column: int,
                 parent: QtWidgets.QWidget = None):
        super().__init__(parent)
        grid.addWidget(self, row, column)
        self.show()


class SelfShowingLineEdit(SelfShowingWidget, QtWidgets.QLineEdit):
    def __init__(self,
                 grid: QtWidgets.QGridLayout,
                 row: int,
                 column: int,
                 parent: QtWidgets.QWidget = None):
        super(SelfShowingLineEdit, self).__init__(grid, row, column, parent)
        super(SelfShowingWidget, self).__init__(parent)
        self.show()


class LoginForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
