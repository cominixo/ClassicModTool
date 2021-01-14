
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from gui.window import Window
from gui.sprite.spritewindow import SpriteWindow

import utils

from pathlib import Path
import platform
import os

app = QApplication(sys.argv)

user_os = platform.system()

carts_path = str(Path.home())

if user_os == "Linux":
    carts_path += "/.lexaloffle/pico-8/carts"
elif user_os == "Windows":
    carts_path = os.getenv('APPDATA') + "\\pico-8\\carts"
elif user_os == "Darwin":
    carts_path += "/Library/Application Support/pico-8/carts"
else:
    print(f"OS Invalid! Was {user_os} (please report this)")
    app.exit(0)
    exit(0)

if not os.path.exists(carts_path):
    carts_path = str(Path.home())


fontid = QFontDatabase.addApplicationFont(utils.fix_path("./assets/pico-8.ttf"))
fontstr = QFontDatabase.applicationFontFamilies(fontid)[0]
font = QFont(fontstr, 10)
app.setFont(font)


cartselector = QFileDialog(None, "Choose a .p8 Celeste cart.", carts_path , "*.p8")
cartselector.setStyleSheet("background-color: #111D35; color: #FFFFFF")

if cartselector.exec_() == QDialog.Accepted:
    cart_file = cartselector.selectedFiles()[0]

    window = Window(cart_file)

else:
    app.exit(0)
    exit(0)

app.exec_()


    