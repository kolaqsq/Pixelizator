import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class MainWindowLight(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindowLight, self).__init__(*args, **kwargs)
        loadUi("MainWindowLight.ui", self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindowLight()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
