from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PIL import Image
import numpy as np

class SpriteTab(QLabel):
    def __init__(self, parent):
        super(SpriteTab, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        
        # TODO tab for misc
        pixmap = self.make_pixmap()
        self.setPixmap(pixmap)
        
        self.resize(pixmap.width(),pixmap.height())

    def make_pixmap(self) -> QPixmap:
        unselected = Image.open('assets/tab-unselected.png').resize((32,32), Image.NEAREST)
        selected = Image.open('assets/tab-selected.png').resize((32,32), Image.NEAREST)


        final = Image.new('RGBA', (112, 32))

        for tab in range(3):
            if self.parent().selected_sprite_tab == tab:
                final.paste(selected, (tab*40, 0))
            else:
                final.paste(unselected, (tab*40, 0))

        img = np.array(final)
        height, width, channel = img.shape
        bytesPerLine = 4 * width
        qImg = QImage(img.data.tobytes(), width, height, bytesPerLine, QImage.Format_RGBA8888)

        return QPixmap(qImg)

    
    def mousePressEvent(self, event):
        tab_clicked = self.mapFromGlobal(event.globalPos()).x()//40
        self.parent().selected_sprite_tab = tab_clicked
        self.parent().spriteselector.load_pages()
        self.setPixmap(self.make_pixmap())
        

        