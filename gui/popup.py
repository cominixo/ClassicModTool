from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Popup(QLabel):
    def __init__(self, parent):
        super(Popup, self).__init__(parent)
        fontid = QFontDatabase.addApplicationFont("assets/pico-8.ttf")
        fontstr = QFontDatabase.applicationFontFamilies(fontid)[0]
        font = QFont(fontstr, 15)
        self.setFont(font)
        
        self.setStyleSheet("color: #FFFFFF")

    def showPopup(self, text):
        self.show()
        self.setText(text)
        QTimer.singleShot(1000, self.hide)