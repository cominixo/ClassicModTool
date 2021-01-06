
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np

from gui.leveldisplay import LevelDisplay
from gui.spriteselector import SpriteSelector
from gui.spritetab import SpriteTab
from cart import Cart


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.drawing = False

        self.cart = Cart("celeste.p8")

        self.selected_sprite = 1
        self.selected_level = 0
        self.selected_sprite_tab = 0

        self.leveldisplay = LevelDisplay(self)
        self.spriteselector = SpriteSelector(self)

        self.button_next = QPushButton('->', self)


        self.button_next.clicked.connect(self.nextLevel)

        self.button_back = QPushButton('<-', self)

        self.button_back.clicked.connect(self.previousLevel)

        self.setMouseTracking(True)

        self.layout = QGridLayout()

        
        self.layout.setVerticalSpacing(0)
        self.layout.addWidget(SpriteTab(self), 0, 1)
        self.layout.addWidget(self.spriteselector,1,1)
        self.layout.addWidget(self.leveldisplay,1,2,2,2)
        self.layout.addWidget(self.button_next,3,3)
        self.layout.addWidget(self.button_back,3,2)
        self.setLayout(self.layout)


        self.setStyleSheet("background-color: black;")

        self.show()

    def nextLevel(self, event):
        self.selected_level += 1
        self.selected_level %= 32
        self.cart.load_map()
        self.leveldisplay.draw_image()

    def previousLevel(self, event):
        self.selected_level -= 1
        self.selected_level %= 32
        self.cart.load_map()
        self.leveldisplay.draw_image()

    def resizeEvent(self, event):
        self.leveldisplay.setPixmap(self.scale_pixmap())

    def mousePressEvent(self, event):
        mouse_pos = self.get_mouse_pos(event.globalPos())
        pixels_per_tile = self.leveldisplay.pixmap().height()/16

        tile_y = int(mouse_pos.y()//pixels_per_tile)
        tile_x = int(mouse_pos.x()//pixels_per_tile)

        if mouse_pos.x() > self.leveldisplay.pixmap().width() or mouse_pos.y() > self.leveldisplay.pixmap().height() or mouse_pos.x() < 0 or mouse_pos.y() < 0:
           return

        self.draw_tile(tile_x, tile_y)
        self.drawing = True

    def mouseReleaseEvent(self, event):
        self.drawing = False

    def mouseMoveEvent(self, event):

        mouse_pos = self.get_mouse_pos(event.globalPos())

        if mouse_pos.x() > self.leveldisplay.pixmap().width() or mouse_pos.y() > self.leveldisplay.pixmap().height() or mouse_pos.x() < 0 or mouse_pos.y() < 0:
           return
        

        pixels_per_tile = self.leveldisplay.pixmap().height()/16

        tile_y = int(mouse_pos.y()//pixels_per_tile)
        tile_x = int(mouse_pos.x()//pixels_per_tile)

        snapped_mouse_pos = QPoint(tile_x*pixels_per_tile, tile_y*pixels_per_tile)

        rect = QRect(snapped_mouse_pos, snapped_mouse_pos + QPoint(pixels_per_tile,pixels_per_tile)) 

        pix = self.leveldisplay.pixmap()

        
        if self.drawing:
            
            self.draw_tile(tile_x, tile_y)

        
        qp = QPainter(pix)
        qp.eraseRect(0, 0, pix.width(), pix.height())
        qp.drawPixmap(QPoint(0,0), self.scale_pixmap())
        img = np.array(self.cart.get_sprite(self.selected_sprite))
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qimg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        qimg = qimg.scaled(QSize(rect.width(), rect.height()))
        qp.setOpacity(0.5)

        qp.drawPixmap(QPoint(tile_x*pixels_per_tile, tile_y*pixels_per_tile), QPixmap().fromImage(qimg))
        



        self.leveldisplay.setPixmap(pix)


    def scale_pixmap(self) -> QPixmap:
        w = self.leveldisplay.width()
        h = self.leveldisplay.height()
        return self.leveldisplay.level_pixmap.scaled(w, h, Qt.KeepAspectRatio)

    def draw_tile(self, tile_x, tile_y):
        qp = QPainter(self.leveldisplay.level_pixmap)
        # TODO change to use current_level
        img = np.array(self.cart.get_sprite(self.selected_sprite))
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qimg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)

        qp.drawPixmap(QPoint(tile_x*8, tile_y*8), QPixmap().fromImage(qimg))

        self.cart.edit_tile(self.selected_sprite, self.selected_level, tile_x, tile_y)
        
        qp.end()
        qp.drawPixmap(QPoint(0,0), self.scale_pixmap())

    def get_mouse_pos(self, global_pos) -> QPoint:
        pixmap_label_difference = (self.leveldisplay.size() - self.leveldisplay.pixmap().size())/2
        difference_point = QPoint(pixmap_label_difference.width(), pixmap_label_difference.height())
        mouse_pos = self.leveldisplay.mapFromGlobal(global_pos)-difference_point
        return mouse_pos

