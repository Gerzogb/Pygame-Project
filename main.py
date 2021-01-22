import sys

import configparser

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
        game.main()
        # self.show()

    def settingsWindow(self):
        self.hide()
        self.w2 = SettingWindow()
        self.w2.show()


class SettingWindow(QWidget):
    def __init__(self):
        super().__init__()
        config = configparser.ConfigParser()
        uic.loadUi('settings.ui', self)
        self.btn_save.clicked.connect(self.save)
        self.btn_back.clicked.connect(self.back)
        self.slide.valueChanged[int].connect(self.changeValue)
        self.val = 100
        self.slide.setMinimum(0)
        self.slide.setMaximum(100)
        config.read("example.ini")
        self.slide.setValue(round(float(config.get("Value", "value")), 1) * 100)

    def save(self):
        config = configparser.ConfigParser()
        config['Value'] = {'value': self.val / 100}
        with open('example.ini', 'w') as configfile:
            config.write(configfile)

    def back(self):
        self.hide()
        ex.show()

    def changeValue(self, value):
        self.val = value

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
