
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from gui.window import Window


app = QApplication(sys.argv)

window = Window()

app.exec_()


    