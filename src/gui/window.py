from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np
import ntpath

from gui.leveldisplay import LevelDisplay
from gui.spriteselector import SpriteSelector
from gui.spritetab import SpriteTab
from gui.button import Button
from gui.sprite.spritewindow import SpriteWindow
from gui.popup import Popup
from cart import Cart
import default_values



class Window(QWidget):
    def __init__(self, cart, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.drawing = False
        self.selecting = False
        self.dragging_box = False
        self.selection_box = QRect()

        self.cart_path = cart
        self.cart = Cart(self.cart_path)
        self.setWindowTitle("ClassicModTool - Editing " + ntpath.basename(cart))

        self.selected_sprite = 1
        self.selected_sprite_alt = 0
        self.selected_level = 0
        self.selected_sprite_tab = 0
        self.selected_tiles = []

        self.autotiled_blocks = []

        self.leveldisplay = LevelDisplay(self)
        self.spriteselector = SpriteSelector(self)

        self.button_next = Button(self, "./assets/next_arrow.png", self.nextLevel)

        self.button_back = Button(self, "./assets/previous_arrow.png", self.previousLevel)

        self.setMouseTracking(True)


        self.saveSc = QShortcut(QKeySequence('Ctrl+S'), self)
        self.saveSc.activated.connect(self.save_cart)

        self.selectSc = QShortcut(QKeySequence('Shift+S'), self)
        self.selectSc.activated.connect(self.setSelecting)

        self.reloadSc = QShortcut(QKeySequence('Ctrl+R'), self)
        self.reloadSc.activated.connect(self.reload_cart)

        self.undoSc = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.undoSc.activated.connect(self.undo)

        self.previousLevelSc = QShortcut(Qt.Key_Left, self)
        self.previousLevelSc.activated.connect(self.previousLevel)

        self.nextLevelSc = QShortcut(Qt.Key_Right, self)
        self.nextLevelSc.activated.connect(self.nextLevel)

        self.layout = QGridLayout()

        self.button_held = 0

        self.sprite_editor = SpriteWindow(self)

        self.selection_button = Button(self, "./assets/selection_button.png", self.setSelecting)
        self.sprite_button = Button(self, "./assets/sprite_button.png", lambda: self.sprite_editor.show())

        self.popup = Popup(self)
        
        self.layout.setVerticalSpacing(0)
        self.layout.addWidget(self.popup,0,3)
        self.layout.addWidget(SpriteTab(self), 0, 0,1,3)
        self.layout.addWidget(self.spriteselector,1,0,3,3)
        self.layout.addWidget(self.selection_button, 4, 0)
        self.layout.addWidget(self.sprite_button, 4, 1)
        self.layout.addWidget(self.leveldisplay,1,2,3,2)
        self.layout.addWidget(self.button_next,4,4)
        self.layout.addWidget(self.button_back,4,3)
        self.setLayout(self.layout)


        self.setStyleSheet("background-color: black;")

        self.show()

    def setSelecting(self):
        self.selected_tiles = []
        self.selecting ^= True
        self.selection_button.draw_image()
        if self.selecting:
            self.selection_button.drawRect(QColor("#C2C3C7"))

        return self.selecting

    def nextLevel(self):
        self.selected_level += 1
        self.selected_level %= 32
        self.cart.load_map()
        self.leveldisplay.draw_image()

    def previousLevel(self):
        self.selected_level -= 1
        self.selected_level %= 32
        self.cart.load_map()
        self.leveldisplay.draw_image()

    def resizeEvent(self, event):
        self.leveldisplay.setPixmap(self.scale_pixmap())

    def undo(self):
        self.cart.undo()
        self.leveldisplay.draw_image()

    def mousePressEvent(self, event):
        mouse_pos = self.get_mouse_pos(event.globalPos())
        pixels_per_tile = self.leveldisplay.pixmap().height()/16

        tile_y = int(mouse_pos.y()//pixels_per_tile)
        tile_x = int(mouse_pos.x()//pixels_per_tile)

        if mouse_pos.x() > self.leveldisplay.pixmap().width() or mouse_pos.y() > self.leveldisplay.pixmap().height() or mouse_pos.x() < 0 or mouse_pos.y() < 0:
           return

        if self.selecting:

            if self.selected_tiles != []:
                for idx, sprite in np.ndenumerate(self.selected_tiles):
                    paste_y, paste_x = idx[0] + tile_y, idx[1] + tile_x
                    self.draw_tile(sprite, paste_x, paste_y)
                modifiers = QApplication.keyboardModifiers()
                if modifiers != Qt.ShiftModifier:
                    self.selected_tiles = []
                self.selection_box = QRect()
                pix = self.leveldisplay.pixmap()
                qp = QPainter(pix)
                qp.eraseRect(0, 0, pix.width(), pix.height())
                qp.drawPixmap(QPoint(0,0), self.scale_pixmap())
                self.leveldisplay.setPixmap(pix)
                return

            if not self.dragging_box:
                self.selection_box.setTopLeft(QPoint(tile_x, tile_y))
                self.dragging_box = True
                return

        
        else:
            if event.button() == Qt.LeftButton:
                if self.selected_sprite < 0:
                    modifiers = QApplication.keyboardModifiers()
                    if modifiers == Qt.ShiftModifier:

                        self.do_autotiling(self.selected_sprite, tile_x, tile_y, False)
                    else:
                        self.do_autotiling(self.selected_sprite, tile_x, tile_y)
                    self.autotiled_blocks.append((tile_x, tile_y))
                else:
                    self.draw_tile(self.selected_sprite, tile_x, tile_y)

            elif event.button() == Qt.RightButton:
                if self.selected_sprite_alt < 0:
                    modifiers = QApplication.keyboardModifiers()
                    if modifiers == Qt.ShiftModifier:

                        self.do_autotiling(self.selected_sprite_alt, tile_x, tile_y, False)
                    else:
                        self.do_autotiling(self.selected_sprite_alt, tile_x, tile_y)
                    self.autotiled_blocks.append((tile_x, tile_y))
                else:
                    self.draw_tile(self.selected_sprite_alt, tile_x, tile_y)


            self.button_held = event.button()
            self.drawing = True

    def mouseReleaseEvent(self, event):

        self.autotiled_blocks = []

        if self.selecting:
            if self.dragging_box:
                if self.selection_box.topLeft().y() > self.selection_box.bottomRight().y():
                    temp = self.selection_box.topLeft()
                    self.selection_box.setTopLeft(self.selection_box.bottomRight())
                    self.selection_box.setBottomRight(temp)
                tiles = np.zeros((abs(self.selection_box.height()), abs(self.selection_box.width())), dtype=np.int32)

                for x in range(abs(self.selection_box.width())):
                    for y in range(abs(self.selection_box.height())):
                        tile_x = x+self.selection_box.x()
                        tile_y = y+self.selection_box.y()

                        if tile_x < 0 or tile_y < 0:
                            break

                        tiles[y][x] = int(self.cart.get_tile(self.selected_level, tile_x, tile_y),16)
                
                self.selected_tiles = tiles
                self.dragging_box = False
                return
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
            if self.button_held == Qt.LeftButton:
                if self.selected_sprite < 0:
                    modifiers = QApplication.keyboardModifiers()
                    if modifiers == Qt.ShiftModifier:

                        self.do_autotiling(self.selected_sprite, tile_x, tile_y, False)
                    else:
                        self.do_autotiling(self.selected_sprite, tile_x, tile_y)
                    self.autotiled_blocks.append((tile_x, tile_y))
                else:
                    self.draw_tile(self.selected_sprite, tile_x, tile_y)
            elif self.button_held == Qt.RightButton:
                if self.selected_sprite_alt < 0:
                    modifiers = QApplication.keyboardModifiers()
                    if modifiers == Qt.ShiftModifier:

                        self.do_autotiling(self.selected_sprite_alt, tile_x, tile_y, False)
                    else:
                        self.do_autotiling(self.selected_sprite_alt, tile_x, tile_y)
                    self.autotiled_blocks.append((tile_x, tile_y))
                else:
                    self.draw_tile(self.selected_sprite_alt, tile_x, tile_y)

        
        qp = QPainter(pix)
        qp.eraseRect(0, 0, pix.width(), pix.height())
        qp.drawPixmap(QPoint(0,0), self.scale_pixmap())

        if self.dragging_box and self.selecting:
            self.update_selection(mouse_pos)
        

        if self.selecting and self.selected_tiles == []:
            
            br = QBrush()
            pen = QPen(QColor("#C2C3C7"))
            pen.setWidth(5)
            pen.setStyle(Qt.DashLine)
            qp.setPen(pen)
            boxscaled = QRect()
           
            boxscaled.setX( self.selection_box.x()*pixels_per_tile)
            boxscaled.setY( self.selection_box.y()*pixels_per_tile)
            boxscaled.setHeight( self.selection_box.height()*pixels_per_tile)
            boxscaled.setWidth( self.selection_box.width()*pixels_per_tile)

            qp.drawRect(boxscaled)
        elif self.selecting:
            for idx, sprite in np.ndenumerate(self.selected_tiles):
                paste_y, paste_x = idx[0] + tile_y, idx[1] + tile_x
                qimg = self.qimage_from_image(self.cart.get_sprite(sprite))
                qimg = qimg.scaled(QSize(rect.width(), rect.height()))
                pixmap =  QPixmap().fromImage(qimg)
                qp.setOpacity(0.5)
                qp.drawPixmap(QPoint(paste_x*pixels_per_tile, paste_y*pixels_per_tile),pixmap)
        else:
            if self.selected_sprite < 0:
                img = self.cart.get_sprite(default_values.autotiling_sprites[self.selected_sprite])
            else:
                img = self.cart.get_sprite(self.selected_sprite)
            
            qp.setOpacity(0.5)

            qimg = self.qimage_from_image(img)
            qimg = qimg.scaled(QSize(rect.width(), rect.height()))

            qp.drawPixmap(QPoint(tile_x*pixels_per_tile, tile_y*pixels_per_tile), QPixmap.fromImage(qimg))
        


        self.leveldisplay.setPixmap(pix)


    def scale_pixmap(self) -> QPixmap:
        w = self.leveldisplay.width()
        h = self.leveldisplay.height()
        return self.leveldisplay.level_pixmap.scaled(w, h, Qt.KeepAspectRatio)

    def draw_tile(self, sprite, tile_x, tile_y):
        qp = QPainter(self.leveldisplay.level_pixmap)

        img = self.cart.get_sprite(sprite)
        qimg = self.qimage_from_image(img)
        qp.drawPixmap(QPoint(tile_x*8, tile_y*8), QPixmap.fromImage(qimg))

        self.cart.edit_tile(sprite, self.selected_level, tile_x, tile_y)
        
        qp.end()
        qp.drawPixmap(QPoint(0,0), self.scale_pixmap())
        self.leveldisplay.setPixmap(self.scale_pixmap())

    def get_mouse_pos(self, global_pos) -> QPoint:
        pixmap_label_difference = (self.leveldisplay.size() - self.leveldisplay.pixmap().size())/2
        difference_point = QPoint(pixmap_label_difference.width(), pixmap_label_difference.height())
        mouse_pos = self.leveldisplay.mapFromGlobal(global_pos)-difference_point
        return mouse_pos

    def update_selection(self, mouse_pos):
        
        pixels_per_tile = self.leveldisplay.pixmap().height()/16

        tile_y = int(mouse_pos.y()//pixels_per_tile)
        tile_x = int(mouse_pos.x()//pixels_per_tile)

        if mouse_pos.x() > self.leveldisplay.pixmap().width() or mouse_pos.y() > self.leveldisplay.pixmap().height() or mouse_pos.x() < 0 or mouse_pos.y() < 0:
           return
        self.selection_box.setBottomRight(QPoint(tile_x, tile_y))

    def qimage_from_image(self, image) -> QImage:
        img = np.array(image)
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qimg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        
        return qimg

    def reload_cart(self):
        self.cart = Cart(self.cart_path)

        
        self.leveldisplay.draw_image()
        for sprite in self.spriteselector.all_sprites:
            sprite.draw_image()
        self.popup.showPopup("reloaded")

    def save_cart(self):
        cart = self.cart.save()
        with open(self.cart_path, "w+") as f:
            f.write(cart)

        self.popup.showPopup("saved")

    def do_autotiling(self, sprite, tile_x, tile_y, globally=True, from_loop=False):

        if sprite < 0:
            sprite = abs(sprite)-1

        if tile_x < 0 or tile_y < 0 or tile_x > 15 or tile_y > 15:
            return

        bitmasking = default_values.blocks_bitmasking[sprite]

        if self.cart.get_tile(self.selected_level, tile_x, tile_y) in bitmasking:
            return

        north_tile = int(self.cart.get_tile(self.selected_level, tile_x, tile_y+1),16)
        west_tile = int(self.cart.get_tile(self.selected_level, tile_x+1, tile_y),16)
        east_tile = int(self.cart.get_tile(self.selected_level, tile_x-1, tile_y),16)
        south_tile = int(self.cart.get_tile(self.selected_level, tile_x, tile_y-1),16) 

        tiles = [((tile_x, tile_y+1),north_tile), ((tile_x+1, tile_y),west_tile), ((tile_x-1, tile_y),east_tile), ((tile_x, tile_y-1),south_tile)]

        bools = []

        if globally:
            bools = [i in bitmasking and 0 <= tile_pos[0] < 16  and 0 <= tile_pos[1] < 16 for tile_pos, i in tiles]
        else:
            bools = [ tile_pos in self.autotiled_blocks and 0 <= tile_pos[0] < 16  and 0 <= tile_pos[1] < 16 for tile_pos, i in tiles]

        

        tile_index_str = ''.join(['1' if i else '0' for i in bools])

        tile = bitmasking[int(tile_index_str, 2)]
        self.draw_tile(tile, tile_x, tile_y)
        if not from_loop:
            if bools[0]:
                self.do_autotiling(sprite, tile_x, tile_y+1, globally, True)
            if bools[1]:
                self.do_autotiling(sprite, tile_x+1, tile_y, globally, True)
            if bools[2]:
                self.do_autotiling(sprite, tile_x-1, tile_y, globally, True)
            if bools[3]:
                self.do_autotiling(sprite, tile_x, tile_y-1, globally, True)

            

        


        

