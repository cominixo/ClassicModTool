from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import math

from consts import P8_COLORS

class ColorSelector(QLabel):
    def __init__(self, parent):
        super(ColorSelector, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.colorpixmap = QPixmap(40*8, 40*2)
        
        self.setPixmap(self.colorpixmap)
        self.setMouseTracking(True)

        self.selected_color = 0
        
        qp = QPainter(self.colorpixmap)

        for color in P8_COLORS:
            r,g,b = color
            index = P8_COLORS.index(color)
            qp.fillRect(QRect(QPoint((index%8)*40, (index//8)*40), QSize(40,40)), QColor(r,g,b))

        self.setPixmap(self.colorpixmap)
        self.resize(40*8, 40*2)
        


    def mouseMoveEvent(self, event):
        pixels_per_tile = 40
        
        floored_pos = QPoint(math.floor(event.localPos().x()), math.floor(event.localPos().y()))
        self.tile_pos = QPoint(floored_pos.x()/pixels_per_tile, floored_pos.y()/pixels_per_tile)

        place_pos = QPoint(self.tile_pos.x()*pixels_per_tile, self.tile_pos.y()*pixels_per_tile)

        self.setPixmap(self.colorpixmap)
        pix = self.pixmap()
        qp = QPainter(pix)
        pen = QPen(Qt.red)
        pen.setWidth(5)
        qp.setPen(pen)
        qp.drawRect(QRect(place_pos, QSize(pixels_per_tile, pixels_per_tile)))

        self.setPixmap(pix)

    def mousePressEvent(self, event):
        colorid = self.tile_pos.x() + 8 * self.tile_pos.y()
        self.selected_color = colorid
