from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ButtonTab(QLabel):
    def __init__(self, parent, buttons):
        super(ButtonTab, self).__init__(parent)

        