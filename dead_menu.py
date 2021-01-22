import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QWidget
import game


class DeadMenu(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('dead_menu.ui', self)
        self.btn_new.clicked.connect(self.new)
        self.btn_ex.clicked.connect(self.ex)

    def new(self):

        game.game_start()
        print(game.running)
        self.hide()

        # self.show()

    def ex(self):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DeadMenu()
    window.show()
    sys.exit(app.exec_())