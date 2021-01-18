import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QWidget


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu.ui', self)  # Загружаем дизайн
        self.btn_play.clicked.connect(self.play)
        self.btn_settings.clicked.connect(self.settingsWindow)

    def play(self):
        self.hide()
        import game
        self.show()

    def settingsWindow(self):
        self.hide()
        import settings
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())