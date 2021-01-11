from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


from gui.sprite.spriteselector import SpriteSelector
from gui.sprite.spritedrawer import SpriteDrawer
from gui.sprite.colorselector import ColorSelector


class SpriteWindow(QWidget):
    def __init__(self, parent, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.layout = QGridLayout()
        self.parent = parent


        self.spriteselector = SpriteSelector(self)
        self.spritedrawer = SpriteDrawer(self)
        self.colorselector = ColorSelector(self)


        self.layout.addWidget(self.spriteselector,0,0)
        self.layout.addWidget(self.spritedrawer,0,1)
        self.layout.addWidget(self.colorselector,0,2)

        self.setStyleSheet("background-color: black;")

        self.setLayout(self.layout)


        

