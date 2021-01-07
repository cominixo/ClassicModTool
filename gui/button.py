from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Button(QLabel):
    def __init__(self, parent, image_path, on_click):
        super(Button, self).__init__(parent)
        self.setPixmap(QPixmap(image_path).scaled(40,40))
        self.on_click = on_click
    
    def mousePressEvent(self, event):
        self.on_click()


