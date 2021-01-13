from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from consts import *
import math

class SpriteSelector(QLabel):
    def __init__(self, parent):
        super(SpriteSelector, self).__init__(parent)

        self.setMouseTracking(True)

        img = self.parent().parent.cart.loaded_spritesheet
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qimg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).scaled(SPRITESHEET_SIZE*3, SPRITESHEET_SIZE*3, Qt.KeepAspectRatio)

        self.spritesheet_pixmap = QPixmap().fromImage(qimg)
        
        self.setPixmap(self.spritesheet_pixmap)
        self.resize(self.pixmap().width(),self.pixmap().height())


    def resizeEvent(self, event):
        self.resize(self.pixmap().width(),self.pixmap().height())

    def mouseMoveEvent(self, event):
        pixels_per_tile = SPRITESHEET_SIZE*3/16
        floored_pos = QPoint(math.floor(event.localPos().x()), math.floor(event.localPos().y()))
        self.tile_pos = QPoint(floored_pos.x()/pixels_per_tile, floored_pos.y()/pixels_per_tile)

        place_pos = QPoint(self.tile_pos.x()*pixels_per_tile, self.tile_pos.y()*pixels_per_tile)

        self.setPixmap(self.spritesheet_pixmap)
        pix = self.pixmap()
        qp = QPainter(pix)
        pen = QPen(Qt.red)
        pen.setWidth(5)
        qp.setPen(pen)
        qp.drawRect(QRect(place_pos, QSize(pixels_per_tile, pixels_per_tile)))

        self.setPixmap(pix)

    def mousePressEvent(self, event):
        spriteid = self.tile_pos.x() + 16 * self.tile_pos.y()
        self.parent().spritedrawer.setSprite(spriteid)


