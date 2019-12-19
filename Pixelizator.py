import sys

from PIL import Image
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap

img = Image.open("alg-img/testimg.jpg")
width, height = img.size


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        loadUi("MainWindow.ui", self)
        self.settings.clicked.connect(lambda: MainWindow.change(self, 1))
        self.settingsHome.clicked.connect(lambda: MainWindow.change(self, 0))
        self.show()

    def change(self, i):
        self.pages.setCurrentIndex(i)

    def init_ui(self):
        self.pixelizationLevelSlider.valueChanged[int].connect(self.changeValue)

    def changeValue(self, value):
        # slider from 1 to 350
        slider = value
        scalew = int((width / 1000) * slider)
        scaleh = int((height / 1000) * slider)

        # Resize smoothly down to scalew x scaleh pixels
        imgSmall = img.resize((scalew, scaleh), resample=Image.BILINEAR)
        # Scale back up using NEAREST to original size
        result = imgSmall.resize(img.size, Image.NEAREST)
        # Save on jpg or png
        result.save('alg-img/result.png')
        self.imageWindow.QPixmap.scaled(self.imageWindow.QPixmap, width, height, aspectRatioMode=4)
        pix = QPixmap('alg-img/result.png')
        self.imageWindow.setPixmap(pix)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    # window.show()
    window.init_ui()
    app.exec_()


if __name__ == '__main__':
    main()
