import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QWidget


class DeadMenu(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('dead_menu.ui', self)
        self.btn_new.clicked.connect(self.new)
        self.btn_ex.clicked.connect(self.ex)

    def new(self):
        self.hide()
        import game
        self.show()

    def ex(self):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DeadMenu()
    ex.show()
    sys.exit(app.exec_())