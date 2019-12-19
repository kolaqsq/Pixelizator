import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        loadUi("MainWindow.ui", self)
        self.settings.clicked.connect(lambda: MainWindow.change(self, 1))
        self.settingsHome.clicked.connect(lambda: MainWindow.change(self, 0))
        self.show()


    def change(self, i):
        self.pages.setCurrentIndex(i)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    # window.show()
    app.exec_()


if __name__ == '__main__':
    main()
