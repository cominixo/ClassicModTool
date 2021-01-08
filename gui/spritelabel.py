from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np

class SpriteLabel(QLabel):
    def __init__(self, parent, spriteid):
        super(SpriteLabel, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.assigned_button = None

        self.spriteid = spriteid
        self.draw_image()
        self.resize(self.sprites_pixmap.width(),self.sprites_pixmap.height())
        

    def draw_image(self):

        
        img = np.array(self.parent().parent().cart.get_sprite(self.spriteid))

        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qImg = QImage(img.data.tobytes(), width, height, bytesPerLine, QImage.Format_RGB888)
        qImg = qImg.scaled(QSize(40,40), aspectRatioMode=Qt.KeepAspectRatio)
        

        self.sprites_pixmap = QPixmap().fromImage(qImg)

        self.setPixmap(self.sprites_pixmap)
    
    # TODO remove rect when another sprite is selected
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent().parent().selected_sprite = self.spriteid
            self.assigned_button = event.button()
            pix = self.drawRect(QColor("#FF004D"))
            self.setPixmap(pix)
        elif event.button() == Qt.RightButton:
            self.parent().parent().selected_sprite_alt = self.spriteid
            self.assigned_button = event.button()
            pix = self.drawRect(QColor("#29ADFF"))
            self.setPixmap(pix)
        self.parent().parent().selecting = False

        for i in self.parent().all_sprites:
            if i.spriteid != self.spriteid and self.assigned_button == i.assigned_button:
                i.draw_image()
        
    def leaveEvent(self, event):
        if not self.assigned_button:
            self.draw_image()
            return self.parent().leaveEvent(event)

    def enterEvent(self, event):

        if not self.assigned_button:
            pix = self.drawRect(Qt.white)
            self.setPixmap(pix)
            return self.parent().enterEvent(event)

    def drawRect(self, color):
        pix = self.pixmap()
        qp = QPainter(pix)
        pen = QPen(color)
        pen.setWidth(5)
        qp.setPen(pen)
        rect = self.rect()
        rect.setHeight(rect.height()-1)
        rect.setWidth(rect.width()-1)
        qp.drawRect(rect)
        
        qp.end()

        return pix

