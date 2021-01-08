from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Button(QLabel):
    def __init__(self, parent, image_path, on_click):
        super(Button, self).__init__(parent)
        self.image_pixmap = QPixmap(image_path).scaled(40,40)
        self.draw_image()
        self.on_click = on_click
        self.resize(self.image_pixmap.width(),self.image_pixmap.height())
    
    def mousePressEvent(self, event):
        self.on_click()
    
    def draw_image(self):
        self.setPixmap(self.image_pixmap)

    def leaveEvent(self, event):
        self.draw_image()
        return self.parent().leaveEvent(event)

    def enterEvent(self, event):
        pix = self.pixmap()
        qp = QPainter(pix)
        pen = QPen(Qt.white)
        pen.setWidth(5)
        qp.setPen(pen)
        rect = self.rect()
        rect.setHeight(40)
        rect.setWidth(40)
        qp.drawRect(rect)
        
        qp.end()
        self.setPixmap(pix)
        return self.parent().enterEvent(event)


