from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np
import math
from consts import P8_COLORS

class SpriteDrawer(QLabel):
    def __init__(self, parent):
        super(SpriteDrawer, self).__init__(parent)
        image = self.parent().parent.cart.get_sprite(1)
        self.selected_sprite = 1
        self.setMouseTracking(True)
        self.setImage(image)


        self.drawing = False

    def mouseMoveEvent(self, event):
        pixels_per_tile = 40
        
        self.tile_pos = self.get_tile_pos(event.localPos())

        place_pos = QPoint(self.tile_pos.x()*pixels_per_tile, self.tile_pos.y()*pixels_per_tile)

        self.setPixmap(self.sprite_pixmap)
        pix = self.pixmap()
        qp = QPainter(pix)
        r,g,b = P8_COLORS[self.parent().colorselector.selected_color]
        qp.fillRect(QRect(place_pos, QSize(pixels_per_tile, pixels_per_tile)),QColor(r,g,b))

        if self.drawing:
            self.drawPixel(self.tile_pos.x(), self.tile_pos.y())

        self.setPixmap(pix)

    def mousePressEvent(self,event):

        self.drawing = True
        self.drawPixel(self.tile_pos.x(), self.tile_pos.y())

        

    def mouseReleaseEvent(self,event):
        self.drawing = False
        

        self.parent().parent.cart.load_spritesheet()
        self.parent().parent.cart.load_map()
        
        self.parent().parent.leveldisplay.draw_image()
        for sprite in self.parent().parent.spriteselector.all_sprites:
            sprite.draw_image()

    def drawPixel(self, x, y):
        qp = QPainter(self.sprite_pixmap)
        color = self.parent().colorselector.selected_color
        r,g,b = P8_COLORS[color]

        pixels_per_tile = 40

        place_pos = QPoint(self.tile_pos.x()*pixels_per_tile, self.tile_pos.y()*pixels_per_tile)

        qp.fillRect(QRect(place_pos, QSize(pixels_per_tile, pixels_per_tile)),QColor(r,g,b))


        self.parent().parent.cart.edit_sprite(color, self.selected_sprite, x, y)

    def get_tile_pos(self, local):
        pixels_per_tile = 40
        
        floored_pos = QPoint(math.floor(local.x()), math.floor(local.y()))
        self.tile_pos = QPoint(floored_pos.x()/pixels_per_tile, floored_pos.y()/pixels_per_tile)
        return self.tile_pos

        
    def resizeEvent(self, event):
        self.resize(self.pixmap().width(),self.pixmap().height())

    def setImage(self, image):
        img = np.array(image)
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qimg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).scaled(320, 320, Qt.KeepAspectRatio)

        self.sprite_pixmap = QPixmap().fromImage(qimg)

        self.setPixmap(self.sprite_pixmap)
        self.resize(self.pixmap().width(),self.pixmap().height())

    def setSprite(self,id):
        self.selected_sprite = id
        self.parent().parent.cart.load_spritesheet()

        
        self.setImage(self.parent().parent.cart.get_sprite(id))

