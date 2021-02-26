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
        self.setFixedWidth(190)

        self.all_sprites = [SpriteLabel(self, i) for i in range(256)]

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


        calculated_width = 150 + 40 * (len(selected_tab) // 20)
        min_width = 190

        self.setFixedWidth(calculated_width if calculated_width>min_width else min_width)
 
        for loaded_sprites in range(len(selected_tab)):
            
            sprite = self.all_sprites[selected_tab[loaded_sprites]]
            if selected_tab[loaded_sprites] < 0:
                sprite = SpriteLabel(self, selected_tab[loaded_sprites])
                self.all_sprites.append(sprite)
         
            

            sprite.setVisible(True)
            self.layout.addWidget(sprite,loaded_sprites%20, loaded_sprites//20)


