from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np

class SpriteLabel(QLabel):
    def __init__(self, parent, spriteid):
        super(SpriteLabel, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

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
    

    def mousePressEvent(self, event):
        self.parent().parent().selected_sprite = self.spriteid
        self.parent().parent().setSelecting()
        print(self.spriteid)

