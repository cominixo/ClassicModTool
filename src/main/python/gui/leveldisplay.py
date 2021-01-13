from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class LevelDisplay(QLabel):
    def __init__(self, parent):
        super(LevelDisplay, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumWidth(100)


        self.setMouseTracking(True)


        self.draw_image()

        self.adjustSize()

    def draw_image(self):

        
        img = self.parent().cart.get_level(self.parent().selected_level)


        height, width, channel = img.shape
        bytesPerLine = 4 * width
        qImg = QImage(img.data.tobytes(), width, height, bytesPerLine, QImage.Format_RGBA8888)
        

        self.level_pixmap = QPixmap().fromImage(qImg)

        w = self.width()
        h = self.height()
        self.setPixmap(self.level_pixmap.scaled(w, h, Qt.KeepAspectRatio))

    def sizeHint(self):
        return QSize(500, 500) 