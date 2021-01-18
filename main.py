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
        self.w2 = SettingWindow()
        self.w2.show()


class SettingWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('settings.ui', self)
        self.btn_save.clicked.connect(self.save)
        self.btn_back.clicked.connect(self.back)

    def save(self):
        pass

    def back(self):
        self.hide()
        ex.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
