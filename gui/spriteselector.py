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

        self.shown_sprites = []

        self.layout = QGridLayout()

        self.load_pages()

        self.setStyleSheet("background-color: #1D2B53;")
        self.layout.setHorizontalSpacing(0)

        self.setLayout(self.layout)


    def resizeEvent(self, event):

        self.load_pages()

    def load_pages(self):

        #loaded_sprites = 0

        selected_tab = default_values.objects

        for sprite in self.shown_sprites:
            self.layout.removeWidget(sprite)

        self.shown_sprites = []

        if self.parent().selected_sprite_tab == 1:
            selected_tab = default_values.blocks
        elif self.parent().selected_sprite_tab == 2:
            selected_tab = default_values.background

        for loaded_sprites in range(len(selected_tab)):
         
            
            sprite = SpriteLabel(self, selected_tab[loaded_sprites])

            self.shown_sprites.append(sprite)

            self.layout.addWidget(sprite,loaded_sprites%20, loaded_sprites//20)


