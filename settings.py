import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QWidget


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('settings.ui', self)
        self.btn_save.clicked.connect(self.save)

    def save(self):
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
