from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from gui.spritelabel import SpriteLabel
from gui.spritetab import SpriteTab
import default_values

import numpy as np

class SpriteSelector(QLabel):
    def __init__(self, parent):
        super(SpriteSelector, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        
        self.setAlignment(Qt.AlignLeft)
        self.setFixedWidth(150)

        self.all_sprites = [SpriteLabel(self, i) for i in range(128)]

        self.shown_sprites = []

        self.layout = QGridLayout()

        self.load_pages()

        self.setStyleSheet("background-color: #1D2B53;")
        self.layout.setHorizontalSpacing(0)

        

        self.setLayout(self.layout)


    def resizeEvent(self, event):

        self.load_pages()

    def load_pages(self):

        for sprite in self.all_sprites:
            sprite.setVisible(False)

        selected_tab = default_values.categories_map[self.parent().selected_sprite_tab]
 
        for loaded_sprites in range(len(selected_tab)):

            if selected_tab[loaded_sprites] < 0:
                self.all_sprites.append(SpriteLabel(self, selected_tab[loaded_sprites]))
         
            sprite = self.all_sprites[selected_tab[loaded_sprites]]

            sprite.setVisible(True)
            self.layout.addWidget(sprite,loaded_sprites%20, loaded_sprites//20)


