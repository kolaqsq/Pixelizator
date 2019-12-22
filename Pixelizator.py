import os.path
import shutil
import sys

from PIL import Image
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QUrl, QPointF
from PyQt5.QtGui import QPixmap, QDesktopServices, QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.uic import loadUi


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        loadUi("testMain.ui", self)

        styleSheetStr = open('light.css', "r").read()
        self.mainPage.setStyleSheet(styleSheetStr)
        self.settingsPage.setStyleSheet(styleSheetStr)
        self.titlebar.setStyleSheet(styleSheetStr)

        self.setWindowFlags(Qt.CustomizeWindowHint)

        self.settings.clicked.connect(lambda: MainWindow.change(self, 1))
        self.settingsHome.clicked.connect(lambda: MainWindow.change(self, 0))
        self.checkBoxTheme.stateChanged.connect(lambda: self.changeTheme())

        self.minimize.clicked.connect(lambda: self.showMinimized())
        self.maximize.clicked.connect(lambda: self.maxRestore())
        self.exit.clicked.connect(self.close)
        self.show()

    def change(self, i):
        self.pages.setCurrentIndex(i)

    def changeTheme(self):
        if self.checkBoxTheme.isChecked() == True:
            styleSheetStr = open('dark.css', "r").read()
            self.mainPage.setStyleSheet(styleSheetStr)
            self.settingsPage.setStyleSheet(styleSheetStr)
            self.titlebar.setStyleSheet(styleSheetStr)

            self.settingsHome.setIcon(QIcon('sources/homeDark.png'))
            self.settingsSettings.setIcon(QIcon('sources/settingsDark.png'))
            self.home.setIcon(QIcon('sources/homeDark.png'))
            self.settings.setIcon(QIcon('sources/settingsDark.png'))
            self.minimize.setIcon(QIcon('sources/minimizeDark.png'))
            self.maximize.setIcon(QIcon('sources/maximizeDark.png'))
            self.exit.setIcon(QIcon('sources/exitDark.png'))
        else:
            styleSheetStr = open('light.css', "r").read()
            self.mainPage.setStyleSheet(styleSheetStr)
            self.settingsPage.setStyleSheet(styleSheetStr)
            self.titlebar.setStyleSheet(styleSheetStr)

            self.settingsHome.setIcon(QIcon('sources/homeLight.png'))
            self.settingsSettings.setIcon(QIcon('sources/settingsLight.png'))
            self.home.setIcon(QIcon('sources/homeLight.png'))
            self.settings.setIcon(QIcon('sources/settingsLight.png'))
            self.minimize.setIcon(QIcon('sources/minimizeLight.png'))
            self.maximize.setIcon(QIcon('sources/maximizeLight.png'))
            self.exit.setIcon(QIcon('sources/exitLight.png'))

    def maxRestore(self):
        global mode
        if mode:
            self.showMaximized()
            mode = False
        else:
            self.showNormal()
            mode = True

    def mousePressEvent(self, event):
        if QPointF.y(event.localPos()) <= QPointF.y(QPointF(0.0, 30.0)) and event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()
        else:
            self.moving = False

    def mouseMoveEvent(self, event):
        if self.moving:
            self.move(event.globalPos() - self.offset)

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

        result = imgSmall.convert("P", palette=Image.ADAPTIVE).resize(img.size,
                                                                      Image.NEAREST)  # Scale back up using NEAREST to original size
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

        result = imgSmall.convert("P", palette=Image.ADAPTIVE).resize(img.size,
                                                                      Image.NEAREST)  # Scale back up using NEAREST to original size
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

        result = imgSmall.convert("P", palette=Image.ADAPTIVE).resize(img.size,
                                                                      Image.NEAREST)  # Scale back up using NEAREST to original size
        result.save('alg-img/result.png')  # Save on jpg or png
        self.changeScale()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.showPicOn()
    window.init_ui()
    app.exec_()


mode = True
if __name__ == '__main__':
    main()
