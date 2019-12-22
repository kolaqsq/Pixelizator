import os.path
import shutil
import sys

from PIL import Image
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap, QDesktopServices, QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.uic import loadUi


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        loadUi("MainWindow.ui", self)

        styleSheetStr = open('light.css', "r").read()
        self.mainPage.setStyleSheet(styleSheetStr)
        self.settingsPage.setStyleSheet(styleSheetStr)

        self.settings.clicked.connect(lambda: MainWindow.change(self, 1))
        self.settingsHome.clicked.connect(lambda: MainWindow.change(self, 0))

        self.checkBoxTheme.stateChanged.connect(lambda: self.changeTheme())
        self.show()

    def change(self, i):
        self.pages.setCurrentIndex(i)

    def init_ui(self):
        self.pixelizationLevelSlider.valueChanged[int].connect(self.changeValue)
        self.chooseBtn.clicked.connect(self.showOpenDialog)
        self.saveBtn.clicked.connect(self.showSaveDialog)
        self.aboutLink.linkActivated.connect(self.link)
        self.aboutLink.setText('<a href="https://github.com/kolaqsq/Pixelizator">Наш Github</a>')

    def changeValue(self, value):
        # slider from 1 to 350
        img = Image.open('alg-img/algimg.jpg')
        width, height = img.size

        slider = value
        scalew = int((width / 1000) * slider)
        scaleh = int((height / 1000) * slider)

        # if user choose little picture
        if scalew <= 0:
            scalew = 1
        if scaleh <= 0:
            scaleh = 1

        # Resize smoothly down to scalew x scaleh pixels
        imgSmall = img.resize((scalew, scaleh), resample=Image.BILINEAR)

        result = imgSmall.convert("P", palette=Image.ADAPTIVE).resize(img.size, Image.NEAREST)  # Scale back up using NEAREST to original size
        result.save('alg-img/result.png')  # Save on jpg or png
        self.changeScale()

    def resizeEvent(self, event):
        self.changeScale()

    def changeScale(self):
        pix = QPixmap('alg-img/result.png')
        pix = pix.scaled(self.imageWindow.size(), Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.imageWindow.setPixmap(pix)

    def showOpenDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.png)")[0]
        # if button close pushed
        if fname != '':
            shutil.copyfile(fname, r'alg-img/algimg.jpg')
            self.showPic()

    def showPic(self):
        img = Image.open('alg-img/algimg.jpg')
        width, height = img.size

        slider = 100
        scalew = int((width / 1000) * slider)
        scaleh = int((height / 1000) * slider)

        # Resize smoothly down to scalew x scaleh pixels
        imgSmall = img.resize((scalew, scaleh), resample=Image.BILINEAR)

        result = imgSmall.resize(img.size, Image.NEAREST)  # Scale back up using NEAREST to original size
        result.save('alg-img/result.png')  # Save on jpg or png
        self.changeScale()

    def showSaveDialog(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file', 'c:\\', "Image files (*.png)")[0]
        # if user want to save nonexistent file
        if os.path.isfile('alg-img/result.png') and fname != '':
            shutil.move('alg-img/result.png', fname)

    def link(self, linkStr):
        QDesktopServices.openUrl(QUrl(linkStr))

    def showPicOn(self):
        img = Image.open('alg-img/begin.jpg')
        shutil.copyfile('alg-img/begin.jpg', r'alg-img/algimg.jpg')
        width, height = img.size

        slider = 100
        scalew = int((width / 1000) * slider)
        scaleh = int((height / 1000) * slider)

        # Resize smoothly down to scalew x scaleh pixels
        imgSmall = img.resize((scalew, scaleh), resample=Image.BILINEAR)

        result = imgSmall.resize(img.size, Image.NEAREST)  # Scale back up using NEAREST to original size
        result.save('alg-img/result.png')  # Save on jpg or png
        self.changeScale()

    def changeTheme(self):
        if self.checkBoxTheme.isChecked() == True:
            styleSheetStr = open('dark.css', "r").read()
            self.mainPage.setStyleSheet(styleSheetStr)
            self.settingsPage.setStyleSheet(styleSheetStr)

            self.settingsHome.setIcon(QIcon('images/iconHomeLight.png'))
            self.settingsSettings.setIcon(QIcon('images/iconSettingsLight.png'))
            self.home.setIcon(QIcon('images/iconHomeLight.png'))
            self.settings.setIcon(QIcon('images/iconSettingsLight.png'))
        else:
            styleSheetStr = open('light.css', "r").read()
            self.mainPage.setStyleSheet(styleSheetStr)
            self.settingsPage.setStyleSheet(styleSheetStr)

            self.settingsHome.setIcon(QIcon('images/iconHome.png'))
            self.settingsSettings.setIcon(QIcon('images/iconSettings.png'))
            self.home.setIcon(QIcon('images/iconHome.png'))
            self.settings.setIcon(QIcon('images/iconSettings.png'))
        print(1)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.showPicOn()
    window.init_ui()
    app.exec_()


if __name__ == '__main__':
    main()
